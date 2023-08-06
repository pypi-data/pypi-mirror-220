import os.path

import torch
import numpy as np
from examples.gnn_dispatch import global_util
from examples.gnn_dispatch.my_memory import MyMemory
from jssp_tool.rl.ppo.memory import Memory
from jssp_tool.util import logger
from tensorboardX import SummaryWriter


class Runner:
    def __init__(self, configs, env, vali_data):
        self.configs = configs
        self.output = os.path.join(global_util.get_project_root(), self.configs.output)
        self.model_dir = os.path.join(self.output, configs.model_dir)
        os.makedirs(self.model_dir, exist_ok=True)

        self.env = env
        self.vali_data = vali_data
        self.device = configs.device
        self.writer = SummaryWriter()
        self.gamma = configs.gamma

    def to_tensor(self, adj, fea, candidate, mask):
        adj_tensor = torch.from_numpy(np.copy(adj)).to(self.device).to_sparse()
        fea_tensor = torch.from_numpy(np.copy(fea)).to(self.device)
        candidate_tensor = torch.from_numpy(np.copy(candidate)).to(self.device).unsqueeze(0)
        mask_tensor = torch.from_numpy(np.copy(mask)).to(self.device).unsqueeze(0)
        return adj_tensor, fea_tensor, candidate_tensor, mask_tensor

    def collect_data(self, ppo, memories, ep_rewards, ep_makespan):
        with torch.no_grad():
            for i in range(self.configs.num_envs):
                obs, _ = self.env.reset()
                obs = self.to_tensor(*obs)
                done = False
                while not done:
                    pi, value = ppo.policy_old(obs)
                    action, a_idx, logprob = ppo.sample_action(pi, obs[2])
                    next_obs, reward, done, _, _ = self.env.step(action.item())
                    next_obs = self.to_tensor(*next_obs)
                    memories[i].append(obs, a_idx, reward, done, logprob, value)
                    obs = next_obs

                    ep_rewards[i] += reward
                memories[i].compute_monte_carlo_returns(self.gamma)
                ep_makespan[i] = self.env.cur_make_span

    def train(self, agent):
        validation_log = []
        memories = [MyMemory() for _ in range(self.configs.num_envs)]
        best_result = float("inf")
        for i_update in range(self.configs.max_updates):
            ep_rewards = [0 for _ in range(self.configs.num_envs)]
            ep_makespan = [0 for _ in range(self.configs.num_envs)]

            # 收集数据
            self.collect_data(agent, memories, ep_rewards, ep_makespan)
            # 训练模型
            v_loss, a_loss, e_loss = agent.update(memories)
            loss_sum = v_loss + a_loss + e_loss
            for memory in memories:
                memory.clear_memory()

            # 以下均为记录或者验证
            mean_ep_reward = sum(ep_rewards) / len(ep_rewards)

            # log results
            logger.info(
                "Episode {}\t Last reward: {:.2f}\t loss: {:.8f}\t make span:{}".format(
                    i_update + 1, mean_ep_reward, loss_sum, sum(ep_makespan) / len(ep_makespan)
                )
            )
            self.writer.add_scalar("train/reward", mean_ep_reward, i_update)
            self.writer.add_scalar("train/loss", loss_sum, i_update)
            self.writer.add_scalar("train/make_span", sum(ep_makespan) / len(ep_makespan), i_update)

            if (i_update + 1) % self.configs.val_frequency == 0:
                best_result = self.test(self.vali_data, agent, validation_log, best_result, i_update)

    def test(self, vali_data, ppo, validation_log, best_result, i_update):
        make_spans = []
        for data in vali_data:
            obs, _ = self.env.reset(data=data)
            rewards = 0
            while True:
                obs = self.to_tensor(*obs)
                with torch.no_grad():
                    pi, _ = ppo.model(obs)
                action = ppo.greedy_select_action(pi, obs[2])
                obs, reward, done, _, _ = self.env.step(action.item())
                rewards += reward
                if done:
                    break
            make_spans.append(self.env.cur_make_span)

        avg_makespan = np.mean(make_spans)
        validation_log.append(avg_makespan)
        if avg_makespan < best_result:
            torch.save(ppo.model.state_dict(), os.path.join(self.output, "best.pth"))
            best_result = avg_makespan
        logger.info("i_update: {}, 测试平均制造周期：{}".format(i_update, avg_makespan))
        self.writer.add_scalar("val/平均制造周期", avg_makespan, i_update)
        with open(os.path.join(self.output, "vali.txt"), "w") as f:
            f.write(str(validation_log))

        return best_result
