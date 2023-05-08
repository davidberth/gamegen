import gymnasium as gym

from stable_baselines3 import PPO

env = gym.make("CartPole-v1", render_mode="human")

model = PPO.load("models/PPO_100000.zip")
episodes = 10
for ep in range(episodes):
    obs, _ = env.reset()
    done = False
    while not done:
        env.render()
        action, _ = model.predict(obs)
        obs, rewards, done, trunc, info = env.step(action)

        
env.close()
        