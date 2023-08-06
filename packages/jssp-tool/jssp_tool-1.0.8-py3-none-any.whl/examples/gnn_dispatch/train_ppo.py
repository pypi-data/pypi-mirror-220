import os.path

from env.jssp_env import JsspEnv
import torch
import numpy as np
from Params import configs
from examples.gnn_dispatch import global_util
from examples.gnn_dispatch.models.actor_critic import ActorCritic
from examples.gnn_dispatch.runner import Runner
from jssp_tool.env.util import set_random_seed
from jssp_tool.rl.ppo.ppo_discrete import PPODiscrete

device = torch.device(configs.device)


def build_ppo(model):
    optimizer = torch.optim.Adam(model.parameters(), lr=configs.lr)
    return PPODiscrete(
        model,
        configs.eps_clip,
        configs.k_epochs,
        optimizer,
        configs.ploss_coef,
        configs.vloss_coef,
        configs.entloss_coef,
        device=configs.device
    )


def main():
    set_random_seed(configs.torch_seed)

    env = JsspEnv(configs.n_j, configs.n_m, configs.low, configs.high, configs.device)
    vali_data = np.load(
        os.path.join(global_util.get_project_root(), "data", "generatedData{}_{}_Seed{}.npy").format(
            configs.n_j, configs.n_m, configs.np_seed_validation
        )
    )

    model = ActorCritic(
        n_j=configs.n_j,
        n_m=configs.n_m,
        num_layers=configs.num_layers,
        learn_eps=False,
        input_dim=configs.input_dim,
        hidden_dim=configs.hidden_dim,
        num_mlp_layers_feature_extract=configs.num_mlp_layers_feature_extract,
        num_mlp_layers_actor=configs.num_mlp_layers_actor,
        hidden_dim_actor=configs.hidden_dim_actor,
        num_mlp_layers_critic=configs.num_mlp_layers_critic,
        hidden_dim_critic=configs.hidden_dim_critic,
        device=device,
    )
    ppo = build_ppo(model)

    configs.output = os.path.join(
        configs.output, "j{}_m{}_l{}_h{}".format(configs.n_j, configs.n_m, configs.low, configs.high)
    )
    runner = Runner(configs, env, vali_data)
    runner.train(ppo)


if __name__ == "__main__":
    main()
