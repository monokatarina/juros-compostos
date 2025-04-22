import gymnasium as gym
from gymnasium import spaces
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv, VecMonitor
import torch
import os

# ====================== 1. Ambiente Personalizado ======================
class MultiAgentChargeEnv(gym.Env):
    def __init__(self, grid_size=10, num_agents=2):
        super().__init__()
        self.grid_size = grid_size
        self.num_agents = num_agents
        self.charge_pos = np.array([2, 2])  # Ponto de carga fixo
        self.unload_pos = np.array([8, 8])  # Ponto de descarga fixo

        # Espaço de observação: posição (x, y) + status de carga (0 ou 1) para cada agente
        self.observation_space = spaces.Dict({
            f"agent_{i}": spaces.Dict({
                "position": spaces.Box(low=0, high=grid_size-1, shape=(2,), dtype=int),
                "has_cargo": spaces.Discrete(2)  # 0 ou 1
            }) for i in range(num_agents)
        })

        # Espaço de ação: cada agente tem 4 ações (cima, baixo, esquerda, direita)
        self.action_space = spaces.MultiDiscrete([4] * num_agents)

    def reset(self):
        self.agents_pos = np.random.randint(0, self.grid_size, size=(self.num_agents, 2))
        self.agents_cargo = np.zeros(self.num_agents, dtype=int)
        return self._get_obs()

    def step(self, actions):
        rewards = np.zeros(self.num_agents)
        dones = np.zeros(self.num_agents, dtype=bool)

        # Movimenta cada agente
        for i in range(self.num_agents):
            action = actions[i]
            if action == 0: self.agents_pos[i][1] = min(self.grid_size-1, self.agents_pos[i][1] + 1)  # Cima
            elif action == 1: self.agents_pos[i][1] = max(0, self.agents_pos[i][1] - 1)               # Baixo
            elif action == 2: self.agents_pos[i][0] = max(0, self.agents_pos[i][0] - 1)               # Esquerda
            elif action == 3: self.agents_pos[i][0] = min(self.grid_size-1, self.agents_pos[i][0] + 1) # Direita

            # Recompensas
            rewards[i] = -0.1  # Penalidade por passo (incentiva eficiência)

            # Chegou ao ponto de carga?
            if np.array_equal(self.agents_pos[i], self.charge_pos):
                self.agents_cargo[i] = 1

            # Chegou ao ponto de descarga com carga?
            if np.array_equal(self.agents_pos[i], self.unload_pos) and self.agents_cargo[i]:
                rewards[i] += 10
                dones[i] = True  # Episódio termina para este agente

        # Observações, recompensas, dones (terminou?), infos (vazio)
        return self._get_obs(), rewards, dones, {}

    def _get_obs(self):
        return {f"agent_{i}": {"position": self.agents_pos[i], "has_cargo": self.agents_cargo[i]} 
                for i in range(self.num_agents)}

# ====================== 2. Treinamento Multiagente ======================
if __name__ == "__main__":
    # Configurações
    num_agents = 2  # Número de agentes
    grid_size = 10   # Tamanho do grid
    total_timesteps = 50_000  # Passos de treinamento

    # Criar ambiente vetorizado (paralelismo)
    env = make_vec_env(
        lambda: MultiAgentChargeEnv(grid_size=grid_size, num_agents=num_agents),
        n_envs=4,  # 4 ambientes paralelos para acelerar o treino
        vec_env_cls=SubprocVecEnv
    )
    env = VecMonitor(env)  # Monitoramento de estatísticas

    # Configurar PPO (usando GPU se disponível)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    policy_kwargs = dict(activation_fn=torch.nn.ReLU, net_arch=[64, 64])
    
    model = PPO(
        "MultiInputPolicy",
        env,
        policy_kwargs=policy_kwargs,
        verbose=1,
        device=device,
        n_steps=1024,
        batch_size=256,
        learning_rate=0.0003,
    )

    # Treinar!
    print(f"Treinando {num_agents} agentes por {total_timesteps} passos...")
    model.learn(total_timesteps=total_timesteps)
    model.save("multi_agent_charge")

    # ====================== 3. Testar o Modelo ======================
    print("Testando o modelo treinado...")
    test_env = MultiAgentChargeEnv(grid_size=grid_size, num_agents=num_agents)
    obs = test_env.reset()
    for _ in range(100):
        actions, _ = model.predict(obs)
        obs, rewards, dones, _ = test_env.step(actions)
        print(f"Agente 0: Posição {obs['agent_0']['position']}, Carga {obs['agent_0']['has_cargo']}, Recompensa {rewards[0]}")
        print(f"Agente 1: Posição {obs['agent_1']['position']}, Carga {obs['agent_1']['has_cargo']}, Recompensa {rewards[1]}")
        if any(dones):
            obs = test_env.reset()