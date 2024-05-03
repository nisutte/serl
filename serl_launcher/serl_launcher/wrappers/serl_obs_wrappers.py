import gymnasium as gym
from gymnasium import spaces
from gymnasium.core import ObsType, WrapperObsType
from gymnasium.spaces import flatten_space, flatten


class SERLObsWrapper(gym.ObservationWrapper):
    """
    This observation wrapper treats the observation space as a dictionary
    of a flattened state space and the images.
    """

    def __init__(self, env):
        super().__init__(env)
        self.observation_space = gym.spaces.Dict(
            {
                "state": flatten_space(self.env.observation_space["state"]),
                **(self.env.observation_space["images"]),
            }
        )

    def observation(self, obs):
        obs = {
            "state": flatten(self.env.observation_space["state"], obs["state"]),
            **(obs["images"]),
        }
        return obs


class SerlObsWrapperNoImages(gym.ObservationWrapper):
    """
    This observation wrapper treats the observation space as a flattened state
    space, if no images are present.
    """

    def __init__(self, env):
        super().__init__(env)
        self.observation_space = flatten_space(self.env.observation_space["state"])

    def observation(self, obs):
        obs = flatten(self.env.observation_space["state"], obs["state"])
        return obs


class ScaleObservationWrapper(gym.ObservationWrapper):

    """
    This observation wrapper scales the observations with the provided hyperparams
    (to somewhat normalize the observations space)
    """
    def __init__(self,
                 env,
                 translation_scale=10.,
                 rotation_scale=10.,
                 velocity_scale=10.,
                 rotational_velocity_scale=10.,
                 force_scale=1.,
                 torque_scale=10.
                 ):
        super().__init__(env)
        self.translation_scale = translation_scale
        self.rotation_scale = rotation_scale
        self.velocity_scale = velocity_scale
        self.rotational_velocity_scale = rotational_velocity_scale
        self.force_scale = force_scale
        self.torque_scale = torque_scale

    def observation(self, obs) -> WrapperObsType:
        obs["state"]["tcp_pose"][:3] *= self.translation_scale
        obs["state"]["tcp_pose"][3:] *= self.rotation_scale
        obs["state"]["tcp_vel"][:3] *= self.velocity_scale
        obs["state"]["tcp_vel"][3:] *= self.rotational_velocity_scale
        obs["state"]["tcp_force"] *= self.force_scale
        obs["state"]["tcp_torque"] *= self.torque_scale
        return obs
