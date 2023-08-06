import copy
import random
import torch
from torch.distributions.categorical import Categorical


class DDQN:
    def __init_(
        self,
        model,
        optimizer,
        batch_size,
        target_update_interval,
        gamma,
        action_dim,
        epsilon_strategy,
        replay_buffer,
        soft_update_tau,
        device=None,
        optimizer_scheduler=None,
        max_grad_norm=None,
    ):
        """
        DDQN算法
        Args:
            model: 神经网络模型
            target_update_interval: 更新model模型参数到target_model的间隔
            gamma: discount factor
            optimizer: adam
            action_dim: 动作维度
            epsilon_strategy: epsilon下降策略
            soft_update_tau: 更新target policy的tau
            device:

        Returns:

        """
        self.model = model
        self.optimizer = optimizer
        self.batch_size = batch_size
        self.target_update_interval = target_update_interval
        self.gamma = gamma
        self.action_dim = action_dim
        self.epsilon_strategy = epsilon_strategy
        self.replay_buffer = replay_buffer
        self.soft_update_tau = soft_update_tau
        self.device = device
        self.optimizer_scheduler = optimizer_scheduler
        self.max_grad_norm = max_grad_norm

        self.target_model = copy.deepcopy(self.model)
        self.target_model.eval()
        self.t = 0

    def learn(self) -> float:
        # 从replay buffer获取数据
        obs_batch, action_batch, reward_batch, next_obs_batch, done_batch = self.replay_buffer.sample(self.batch_size)
        loss = self._update(obs_batch, action_batch, reward_batch, next_obs_batch, done_batch)
        return loss

    def select_action(self, obs_batch, greedy=False, sample=False, q_factor=1.0):
        if greedy:
            return self._greedy_select_action(obs_batch, sample, q_factor)
        else:
            if random.random() < self.epsilon_strategy.epsilon:
                return self._random_select_action()
            else:
                return self._greedy_select_action(obs_batch, sample, q_factor)

    def _update(
        self, obs_batch, action_batch, reward_batch, next_obs_batch, done_batch, clip_delta=False, accumulator="mean"
    ):
        self.t += 1

        # 计算y
        qout = self.model(obs_batch)
        q_values = qout.gather(dim=1, index=action_batch)
        # 计算truth
        qout_next = self.target_model(next_obs_batch)
        qout_next_max = qout_next.max
        q_values_next = reward_batch + self.gamma * (1.0 - done_batch) * qout_next_max

        assert accumulator in ("mean", "sum")
        y = q_values.reshape(-1, 1)
        t = q_values_next.reshape(-1, 1)
        if clip_delta:
            loss = torch.nn.functional.smooth_l1_loss(y, t, reduction=accumulator)
        else:
            loss = torch.nn.functional.mse_loss(y, t, reduction=accumulator) / 2

        # 反向传播，更新模型参数
        self.optimizer.zero_grad()
        loss.backward()
        if self.max_grad_norm is not None:
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.max_grad_norm)
        self.optimizer.step()
        if self.optimizer_scheduler is not None:
            self.optimizer_scheduler.step()

        # 更新target model
        if self.t % self.target_update_interval == 0:
            self._soft_update_target_model()

        self.epsilon_strategy.update_epsilon()

        return loss.item()

    def _greedy_select_action(self, obs_batch, sample=False, q_factor=1.0):
        """
        选择Q值最大的动作或者根据Q值采样动作
        Args:
            obs_batch: shape: (batch_size,*obs_shape)
            sample (bool): 是否用采样的方式。默认False，表示选取Q值最大的动作

        Returns:
            action
        """
        q_values = self.model(obs_batch)
        q_values = q_values * q_factor
        if sample:
            probabilities = torch.nn.functional.softmax(q_values, dim=1)
            categories = Categorical(probabilities.squeeze())
            return categories.sample()
        else:
            return torch.argmax(q_values, dim=1)

    def _random_select_action(self):
        return random.randint(0, self.action_dim)

    def _soft_update_target_model(self):
        source_dict = self.model.state_dict()
        target_dict = self.target_model.state_dict()
        for k, target_value in target_dict.items():
            source_value = source_dict[k]
            if source_value.dtype in [torch.float32, torch.float64, torch.float16]:
                assert target_value.shape == source_value.shape
                target_value.mul_(1 - self.soft_update_tau)
                target_value.add_(self.soft_update_tau * source_value)
            else:
                # Scalar type
                # Some modules such as BN has scalar value `num_batches_tracked`
                target_dict[k] = source_value
