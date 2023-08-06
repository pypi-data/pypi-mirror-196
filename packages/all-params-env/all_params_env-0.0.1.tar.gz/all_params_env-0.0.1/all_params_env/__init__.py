from gym.envs.registration import register

register(
    id="all_params_env-v0",
    entry_point='all_params_env.envs:all_params_env'
)