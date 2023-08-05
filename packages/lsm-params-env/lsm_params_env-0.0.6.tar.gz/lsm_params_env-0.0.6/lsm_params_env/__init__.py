from gym.envs.registration import register

register(
    id='lsm_params_env-v0',
    entry_point='lsm_params_env.envs:ParamsEnv'
)