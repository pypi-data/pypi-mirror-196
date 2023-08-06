from gym.envs.registration import register

register(
    id='Lsm_all_params_env-v0',
    entry_points='Lsm_all_params_env.envs:all_params_env'
)