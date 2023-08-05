import math
from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple

import torch
import torch.nn.functional as F
from torch.distributions import Normal

__all__ = [
    "Distribution",
    "GaussianDistribution",
    "SquashedGaussianDistribution",
]


class Distribution(metaclass=ABCMeta):
    @abstractmethod
    def sample(self) -> torch.Tensor:
        pass

    @abstractmethod
    def sample_with_log_prob(self) -> Tuple[torch.Tensor, torch.Tensor]:
        pass

    @abstractmethod
    def sample_n(self, n: int) -> torch.Tensor:
        pass

    @abstractmethod
    def sample_n_with_log_prob(
        self, n: int
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        pass

    @abstractmethod
    def log_prob(self, y: torch.Tensor) -> torch.Tensor:
        pass


class GaussianDistribution(Distribution):
    _raw_loc: torch.Tensor
    _mean: torch.Tensor
    _std: torch.Tensor
    _dist: Normal

    def __init__(
        self,
        loc: torch.Tensor,
        std: torch.Tensor,
        raw_loc: Optional[torch.Tensor] = None,
    ):
        self._mean = loc
        self._std = std
        if raw_loc is not None:
            self._raw_loc = raw_loc
        self._dist = Normal(self._mean, self._std)

    def sample(self) -> torch.Tensor:
        return self._dist.rsample().clamp(-1.0, 1.0)

    def sample_with_log_prob(self) -> Tuple[torch.Tensor, torch.Tensor]:
        y = self.sample()
        return y, self.log_prob(y)

    def sample_without_squash(self) -> torch.Tensor:
        assert self._raw_loc is not None
        return Normal(self._raw_loc, self._std).rsample()

    def sample_n(self, n: int) -> torch.Tensor:
        return self._dist.rsample((n,)).clamp(-1.0, 1.0)

    def sample_n_with_log_prob(
        self, n: int
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        x = self.sample_n(n)
        return x, self.log_prob(x)

    def sample_n_without_squash(self, n: int) -> torch.Tensor:
        assert self._raw_loc is not None
        return Normal(self._raw_loc, self._std).rsample((n,))

    def mean_with_log_prob(self) -> Tuple[torch.Tensor, torch.Tensor]:
        return self._mean, self.log_prob(self._mean)

    def log_prob(self, y: torch.Tensor) -> torch.Tensor:
        return self._dist.log_prob(y).sum(dim=-1, keepdims=True)

    @property
    def mean(self) -> torch.Tensor:
        return self._mean

    @property
    def std(self) -> torch.Tensor:
        return self._std


class SquashedGaussianDistribution(Distribution):
    _mean: torch.Tensor
    _std: torch.Tensor
    _dist: Normal

    def __init__(self, loc: torch.Tensor, std: torch.Tensor):
        self._mean = loc
        self._std = std
        self._dist = Normal(self._mean, self._std)

    def sample(self) -> torch.Tensor:
        return torch.tanh(self._dist.rsample())

    def sample_with_log_prob(self) -> Tuple[torch.Tensor, torch.Tensor]:
        raw_y = self._dist.rsample()
        log_prob = self._log_prob_from_raw_y(raw_y)
        return torch.tanh(raw_y), log_prob

    def sample_without_squash(self) -> torch.Tensor:
        return self._dist.rsample()

    def sample_n(self, n: int) -> torch.Tensor:
        return torch.tanh(self._dist.rsample((n,)))

    def sample_n_with_log_prob(
        self, n: int
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        raw_y = self._dist.rsample((n,))
        log_prob = self._log_prob_from_raw_y(raw_y)
        return torch.tanh(raw_y), log_prob

    def sample_n_without_squash(self, n: int) -> torch.Tensor:
        return self._dist.rsample((n,))

    def mean_with_log_prob(self) -> Tuple[torch.Tensor, torch.Tensor]:
        return torch.tanh(self._mean), self._log_prob_from_raw_y(self._mean)

    def log_prob(self, y: torch.Tensor) -> torch.Tensor:
        clipped_y = y.clamp(-0.999999, 0.999999)
        raw_y = torch.atanh(clipped_y)
        return self._log_prob_from_raw_y(raw_y)

    def _log_prob_from_raw_y(self, raw_y: torch.Tensor) -> torch.Tensor:
        jacob = 2 * (math.log(2) - raw_y - F.softplus(-2 * raw_y))
        return (self._dist.log_prob(raw_y) - jacob).sum(dim=-1, keepdims=True)

    @property
    def mean(self) -> torch.Tensor:
        return torch.tanh(self._mean)

    @property
    def std(self) -> torch.Tensor:
        return self._std
