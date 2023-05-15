import gymnasium as gym
from gymnasium.wrappers import FlattenObservation
import gamegen

from stable_baselines3 import PPO

env = gym.make("gamegen-v0", width=32*20, height = 32*15+30, window_title = 'First agent', controller_type = 'nn', 
               render_mode = 'human')
env = FlattenObservation(env)

model = PPO("MlpPolicy", env, verbose=1)
timesteps = 10000
for i in range(30):
        model.learn(total_timesteps=10_000, reset_num_timesteps = False, tb_log_name="PPO")
        model.save(f"models/PPO_{i*timesteps}")

