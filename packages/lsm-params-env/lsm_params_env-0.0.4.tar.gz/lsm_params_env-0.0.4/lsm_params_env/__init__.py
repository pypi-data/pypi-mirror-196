from gym.envs.registration import register

register(
    id='lsm_params_env',
    entry_point='lsm_params_env.envs:ParamsEnv'
)