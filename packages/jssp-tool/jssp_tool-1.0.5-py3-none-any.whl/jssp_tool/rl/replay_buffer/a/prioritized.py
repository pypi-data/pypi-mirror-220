import collections

import numpy as np
from jssp_tool.rl.replay_buffer.a.random import sample_n_k
from jssp_tool.rl.replay_buffer.a.sum_tree import SumTreeQueue, MinTreeQueue

import collections
from typing import (
    Any,
    Callable,
    Deque,
    Generic,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
)

from jssp_tool.rl.replay_buffer.replay_buffer import ReplayBuffer

T = TypeVar("T")


class PrioritizedBuffer(Generic[T]):
    def __init__(
        self,
        capacity: Optional[int] = None,
        wait_priority_after_sampling: bool = True,
        initial_max_priority: float = 1.0,
    ):
        self.capacity = capacity
        self.data: Deque = collections.deque()
        self.priority_sums = SumTreeQueue()
        self.priority_mins = MinTreeQueue()
        self.max_priority = initial_max_priority
        self.wait_priority_after_sampling = wait_priority_after_sampling
        self.flag_wait_priority = False

    def __len__(self) -> int:
        return len(self.data)

    def append(self, value: T, priority: Optional[float] = None) -> None:
        if self.capacity is not None and len(self) == self.capacity:
            self.popleft()
        if priority is None:
            # Append with the highest priority
            priority = self.max_priority

        self.data.append(value)
        self.priority_sums.append(priority)
        self.priority_mins.append(priority)

    def popleft(self) -> T:
        assert len(self) > 0
        self.priority_sums.popleft()
        self.priority_mins.popleft()
        return self.data.popleft()

    def _sample_indices_and_probabilities(self, n: int, uniform_ratio: float) -> Tuple[List[int], List[float], float]:
        total_priority: float = self.priority_sums.sum()
        min_prob = self.priority_mins.min() / total_priority
        indices = []
        priorities = []
        if uniform_ratio > 0:
            # Mix uniform samples and prioritized samples
            n_uniform = np.random.binomial(n, uniform_ratio)
            un_indices, un_priorities = self.priority_sums.uniform_sample(
                n_uniform, remove=self.wait_priority_after_sampling
            )
            indices.extend(un_indices)
            priorities.extend(un_priorities)
            n -= n_uniform
            min_prob = uniform_ratio / len(self) + (1 - uniform_ratio) * min_prob

        pr_indices, pr_priorities = self.priority_sums.prioritized_sample(n, remove=self.wait_priority_after_sampling)
        indices.extend(pr_indices)
        priorities.extend(pr_priorities)

        probs = [uniform_ratio / len(self) + (1 - uniform_ratio) * pri / total_priority for pri in priorities]
        return indices, probs, min_prob

    def sample(self, n: int, uniform_ratio: float = 0) -> Tuple[List[T], List[float], float]:
        """Sample data along with their corresponding probabilities.

        Args:
            n (int): Number of data to sample.
            uniform_ratio (float): Ratio of uniformly sampled data.
        Returns:
            sampled data (list)
            probabitilies (list)
        """
        assert not self.wait_priority_after_sampling or not self.flag_wait_priority
        indices, probabilities, min_prob = self._sample_indices_and_probabilities(n, uniform_ratio=uniform_ratio)
        sampled = [self.data[i] for i in indices]
        self.sampled_indices = indices
        self.flag_wait_priority = True
        return sampled, probabilities, min_prob

    def set_last_priority(self, priority: Sequence[float]) -> None:
        assert not self.wait_priority_after_sampling or self.flag_wait_priority
        assert all([p > 0.0 for p in priority])
        assert len(self.sampled_indices) == len(priority)
        for i, p in zip(self.sampled_indices, priority):
            self.priority_sums[i] = p
            self.priority_mins[i] = p
            self.max_priority = max(self.max_priority, p)
        self.flag_wait_priority = False
        self.sampled_indices = []

    def _uniform_sample_indices_and_probabilities(self, n: int) -> Tuple[List[int], List[float]]:
        indices = list(sample_n_k(len(self.data), n))
        probabilities = [1 / len(self)] * len(indices)
        return indices, probabilities


class PriorityWeightError(object):
    """For proportional prioritization

    alpha determines how much prioritization is used.

    beta determines how much importance sampling weights are used. beta is
    scheduled by ``beta0`` and ``betasteps``.

    Args:
        alpha (float): Exponent of errors to compute probabilities to sample
        beta0 (float): Initial value of beta
        betasteps (float): Steps to anneal beta to 1
        eps (float): To revisit a step after its error becomes near zero
        normalize_by_max (str): Method to normalize weights. ``'batch'`` or
            ``True`` (default): divide by the maximum weight in the sampled
            batch. ``'memory'``: divide by the maximum weight in the memory.
            ``False``: do not normalize.
    """

    def __init__(self, alpha, beta0, betasteps, eps, normalize_by_max, error_min, error_max):
        assert 0.0 <= alpha
        assert 0.0 <= beta0 <= 1.0
        self.alpha = alpha
        self.beta = beta0
        if betasteps is None:
            self.beta_add = 0
        else:
            self.beta_add = (1.0 - beta0) / betasteps
        self.eps = eps
        if normalize_by_max is True:
            normalize_by_max = "batch"
        assert normalize_by_max in [False, "batch", "memory"]
        self.normalize_by_max = normalize_by_max
        self.error_min = error_min
        self.error_max = error_max

    def priority_from_errors(self, errors):
        def _clip_error(error):
            if self.error_min is not None:
                error = max(self.error_min, error)
            if self.error_max is not None:
                error = min(self.error_max, error)
            return error

        return [(_clip_error(d) + self.eps) ** self.alpha for d in errors]

    def weights_from_probabilities(self, probabilities, min_probability):
        if self.normalize_by_max == "batch":
            # discard global min and compute batch min
            min_probability = np.min(probabilities)
        if self.normalize_by_max:
            weights = [(p / min_probability) ** -self.beta for p in probabilities]
        else:
            weights = [(len(self.memory) * p) ** -self.beta for p in probabilities]
        self.beta = min(1.0, self.beta + self.beta_add)
        return weights


class PrioritizedReplayBuffer(ReplayBuffer, PriorityWeightError):
    """Stochastic Prioritization

    https://arxiv.org/pdf/1511.05952.pdf Section 3.3
    proportional prioritization

    Args:
        capacity (int): capacity in terms of number of transitions
        alpha (float): Exponent of errors to compute probabilities to sample
        beta0 (float): Initial value of beta
        betasteps (int): Steps to anneal beta to 1
        eps (float): To revisit a step after its error becomes near zero
        normalize_by_max (bool): Method to normalize weights. ``'batch'`` or
            ``True`` (default): divide by the maximum weight in the sampled
            batch. ``'memory'``: divide by the maximum weight in the memory.
            ``False``: do not normalize
    """

    def __init__(
        self,
        capacity=None,
        alpha=0.6,
        beta0=0.4,
        betasteps=2e5,
        eps=0.01,
        normalize_by_max=True,
        error_min=0,
        error_max=1,
        num_steps=1,
    ):
        self.capacity = capacity
        assert num_steps > 0
        self.num_steps = num_steps
        self.memory = PrioritizedBuffer(capacity=capacity)
        self.last_n_transitions = collections.defaultdict(lambda: collections.deque([], maxlen=num_steps))
        PriorityWeightError.__init__(
            self,
            alpha,
            beta0,
            betasteps,
            eps,
            normalize_by_max,
            error_min=error_min,
            error_max=error_max,
        )

    def sample(self, n):
        assert len(self.memory) >= n
        sampled, probabilities, min_prob = self.memory.sample(n)
        weights = self.weights_from_probabilities(probabilities, min_prob)
        for e, w in zip(sampled, weights):
            e[0]["weight"] = w
        return sampled

    def update_errors(self, errors):
        self.memory.set_last_priority(self.priority_from_errors(errors))
