import dataclasses
from typing import Dict

import numpy as np

from ...base import DeviceArg, LearnableConfig, register_learnable
from ...constants import ActionSpace
from ...dataset import Observation, Shape
from ...torch_utility import TorchMiniBatch
from .base import QLearningAlgoBase

__all__ = [
    "RandomPolicyConfig",
    "RandomPolicy",
    "DiscreteRandomPolicyConfig",
    "DiscreteRandomPolicy",
]


@dataclasses.dataclass()
class RandomPolicyConfig(LearnableConfig):
    r"""Random Policy for continuous control algorithm.

    This is designed for data collection and lightweight interaction tests.
    ``fit`` and ``fit_online`` methods will raise exceptions.

    Args:
        action_scaler (d3rlpy.preprocessing.ActionScaler): Action preprocessor.
        distribution (str): Random distribution. Available options are
            ``['uniform', 'normal']``.
        normal_std (float): Standard deviation of the normal distribution. This
            is only used when ``distribution='normal'``.
    """
    distribution: str = "uniform"
    normal_std: float = 1.0

    def create(self, device: DeviceArg = False) -> "RandomPolicy":  # type: ignore
        return RandomPolicy(self)

    @staticmethod
    def get_type() -> str:
        return "random_policy"


class RandomPolicy(QLearningAlgoBase[None, RandomPolicyConfig]):  # type: ignore
    _action_size: int

    def __init__(self, config: RandomPolicyConfig):
        super().__init__(config, False, None)
        self._action_size = 1

    def inner_create_impl(
        self, observation_shape: Shape, action_size: int
    ) -> None:
        self._action_size = action_size

    def predict(self, x: Observation) -> np.ndarray:
        return self.sample_action(x)

    def sample_action(self, x: Observation) -> np.ndarray:
        x = np.asarray(x)
        action_shape = (x.shape[0], self._action_size)

        if self._config.distribution == "uniform":
            action = np.random.uniform(-1.0, 1.0, size=action_shape)
        elif self._config.distribution == "normal":
            action = np.random.normal(
                0.0, self._config.normal_std, size=action_shape
            )
        else:
            raise ValueError(
                f"invalid distribution type: {self._config.distribution}"
            )

        action = np.clip(action, -1.0, 1.0)

        if self._config.action_scaler:
            action = self._config.action_scaler.reverse_transform_numpy(action)

        return action

    def predict_value(self, x: Observation, action: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def inner_update(self, batch: TorchMiniBatch) -> Dict[str, float]:
        raise NotImplementedError

    def get_action_type(self) -> ActionSpace:
        return ActionSpace.CONTINUOUS


@dataclasses.dataclass()
class DiscreteRandomPolicyConfig(LearnableConfig):
    r"""Random Policy for discrete control algorithm.

    This is designed for data collection and lightweight interaction tests.
    ``fit`` and ``fit_online`` methods will raise exceptions.
    """

    def create(self, device: DeviceArg = False) -> "DiscreteRandomPolicy":  # type: ignore
        return DiscreteRandomPolicy(self)

    @staticmethod
    def get_type() -> str:
        return "discrete_random_policy"


class DiscreteRandomPolicy(QLearningAlgoBase[None, DiscreteRandomPolicyConfig]):  # type: ignore
    _action_size: int

    def __init__(self, config: DiscreteRandomPolicyConfig):
        super().__init__(config, False, None)
        self._action_size = 1

    def inner_create_impl(
        self, observation_shape: Shape, action_size: int
    ) -> None:
        self._action_size = action_size

    def predict(self, x: Observation) -> np.ndarray:
        return self.sample_action(x)

    def sample_action(self, x: Observation) -> np.ndarray:
        x = np.asarray(x)
        return np.random.randint(self._action_size, size=x.shape[0])

    def predict_value(self, x: Observation, action: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def inner_update(self, batch: TorchMiniBatch) -> Dict[str, float]:
        raise NotImplementedError

    def get_action_type(self) -> ActionSpace:
        return ActionSpace.DISCRETE


register_learnable(RandomPolicyConfig)
register_learnable(DiscreteRandomPolicyConfig)
