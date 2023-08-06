from gym.envs.registration import register

register(
    id='panfoo-v0',
    entry_point='gym_panfoo.envs:PandaEnv',
)