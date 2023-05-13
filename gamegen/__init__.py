from gymnasium.envs.registration import register

register(
    id        = 'gamegen-v0',
    entry_point = 'gamegen.game:Game',
    max_episode_steps=1000,
)