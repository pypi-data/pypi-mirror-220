import random
import torch


class ReplayBuffer:
    """
    记录一个episode数据
    """

    def __init__(self, capacity: int, device):
        self.capacity = capacity
        self.obs_buf = []
        self.actions_buf = []
        self.rewards_buf = []
        self.dones_buf = []
        self.next_obs_buf = []
        self.device = device

    def clear_memory(self):
        del self.obs_buf[:]
        del self.actions_buf[:]
        del self.rewards_buf[:]
        del self.dones_buf[:]
        del self.next_obs_buf[:]

    def append(self, obs, action, reward, next_obs, done):
        if isinstance(obs, tuple):
            if len(self.obs_buf) == 0:
                self.obs_buf = [[] for _ in range(len(obs))]
            for i, item in enumerate(obs):
                self.obs_buf[i].append(item)
        else:
            self.obs_buf.append(obs)
        self.actions_buf.append(action)
        self.rewards_buf.append(reward)
        self.dones_buf.append(done)
        self.next_obs_buf.append(next_obs)

    def sample(self, batch_size):
        size = len(self.obs_buf)
        assert batch_size >= size

        inds = random.choices(range(0, size), k=batch_size)
        obs_batch = self._handle_obs(self.obs_buf[inds])
        action_batch = torch.stack(self.actions_buf[inds]).to(self.device)
        reward_batch = torch.stack(self.rewards_buf[inds]).to(self.device)
        next_obs_batch = self._handle_obs(self.next_obs_buf[inds])
        done_batch = torch.stack(self.dones_buf[inds]).to(self.device)

        return obs_batch, action_batch, reward_batch, next_obs_batch, done_batch

    def _handle_obs(self, obs_batch):
        if isinstance(obs_batch[0], tuple):
            obs_result = []
            for item in obs_batch:
                obs_result.append(torch.stack(item).to(self.device))
            return obs_result
        else:
            return torch.stack(obs_batch).to(self.device)

    def __len__(self):
        return len(self.obs_buf)


