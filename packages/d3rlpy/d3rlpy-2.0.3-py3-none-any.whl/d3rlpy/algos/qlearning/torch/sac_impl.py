import copy
import math
from typing import Tuple

import torch
from torch.optim import Optimizer

from ....dataset import Shape
from ....models.torch import (
    CategoricalPolicy,
    EnsembleContinuousQFunction,
    EnsembleDiscreteQFunction,
    EnsembleQFunction,
    Parameter,
    Policy,
)
from ....torch_utility import TorchMiniBatch, hard_sync, train_api
from ..base import QLearningAlgoImplBase
from .ddpg_impl import DDPGBaseImpl
from .utility import DiscreteQFunctionMixin

__all__ = ["SACImpl", "DiscreteSACImpl"]


class SACImpl(DDPGBaseImpl):
    _log_temp: Parameter
    _temp_optim: Optimizer

    def __init__(
        self,
        observation_shape: Shape,
        action_size: int,
        policy: Policy,
        q_func: EnsembleContinuousQFunction,
        log_temp: Parameter,
        actor_optim: Optimizer,
        critic_optim: Optimizer,
        temp_optim: Optimizer,
        gamma: float,
        tau: float,
        device: str,
    ):
        super().__init__(
            observation_shape=observation_shape,
            action_size=action_size,
            policy=policy,
            q_func=q_func,
            actor_optim=actor_optim,
            critic_optim=critic_optim,
            gamma=gamma,
            tau=tau,
            device=device,
        )
        self._log_temp = log_temp
        self._temp_optim = temp_optim

    def compute_actor_loss(self, batch: TorchMiniBatch) -> torch.Tensor:
        action, log_prob = self._policy.sample_with_log_prob(batch.observations)
        entropy = self._log_temp().exp() * log_prob
        q_t = self._q_func(batch.observations, action, "min")
        return (entropy - q_t).mean()

    @train_api
    def update_temp(self, batch: TorchMiniBatch) -> Tuple[float, float]:
        self._temp_optim.zero_grad()

        with torch.no_grad():
            _, log_prob = self._policy.sample_with_log_prob(batch.observations)
            targ_temp = log_prob - self._action_size

        loss = -(self._log_temp().exp() * targ_temp).mean()

        loss.backward()
        self._temp_optim.step()

        # current temperature value
        cur_temp = self._log_temp().exp().cpu().detach().numpy()[0][0]

        return float(loss.cpu().detach().numpy()), float(cur_temp)

    def compute_target(self, batch: TorchMiniBatch) -> torch.Tensor:
        with torch.no_grad():
            action, log_prob = self._policy.sample_with_log_prob(
                batch.next_observations
            )
            entropy = self._log_temp().exp() * log_prob
            target = self._targ_q_func.compute_target(
                batch.next_observations,
                action,
                reduction="min",
            )
            return target - entropy


class DiscreteSACImpl(DiscreteQFunctionMixin, QLearningAlgoImplBase):
    _policy: CategoricalPolicy
    _q_func: EnsembleDiscreteQFunction
    _targ_q_func: EnsembleDiscreteQFunction
    _log_temp: Parameter
    _actor_optim: Optimizer
    _critic_optim: Optimizer
    _temp_optim: Optimizer

    def __init__(
        self,
        observation_shape: Shape,
        action_size: int,
        q_func: EnsembleDiscreteQFunction,
        policy: CategoricalPolicy,
        log_temp: Parameter,
        actor_optim: Optimizer,
        critic_optim: Optimizer,
        temp_optim: Optimizer,
        gamma: float,
        device: str,
    ):
        super().__init__(
            observation_shape=observation_shape,
            action_size=action_size,
            device=device,
        )
        self._gamma = gamma
        self._q_func = q_func
        self._policy = policy
        self._log_temp = log_temp
        self._actor_optim = actor_optim
        self._critic_optim = critic_optim
        self._temp_optim = temp_optim
        self._targ_q_func = copy.deepcopy(q_func)

    @train_api
    def update_critic(self, batch: TorchMiniBatch) -> float:
        self._critic_optim.zero_grad()

        q_tpn = self.compute_target(batch)
        loss = self.compute_critic_loss(batch, q_tpn)

        loss.backward()
        self._critic_optim.step()

        return float(loss.cpu().detach().numpy())

    def compute_target(self, batch: TorchMiniBatch) -> torch.Tensor:
        with torch.no_grad():
            log_probs = self._policy.log_probs(batch.next_observations)
            probs = log_probs.exp()
            entropy = self._log_temp().exp() * log_probs
            target = self._targ_q_func.compute_target(batch.next_observations)
            keepdims = True
            if target.dim() == 3:
                entropy = entropy.unsqueeze(-1)
                probs = probs.unsqueeze(-1)
                keepdims = False
            return (probs * (target - entropy)).sum(dim=1, keepdim=keepdims)

    def compute_critic_loss(
        self,
        batch: TorchMiniBatch,
        q_tpn: torch.Tensor,
    ) -> torch.Tensor:
        return self._q_func.compute_error(
            observations=batch.observations,
            actions=batch.actions.long(),
            rewards=batch.rewards,
            target=q_tpn,
            terminals=batch.terminals,
            gamma=self._gamma**batch.intervals,
        )

    @train_api
    def update_actor(self, batch: TorchMiniBatch) -> float:
        # Q function should be inference mode for stability
        self._q_func.eval()

        self._actor_optim.zero_grad()

        loss = self.compute_actor_loss(batch)

        loss.backward()
        self._actor_optim.step()

        return float(loss.cpu().detach().numpy())

    def compute_actor_loss(self, batch: TorchMiniBatch) -> torch.Tensor:
        with torch.no_grad():
            q_t = self._q_func(batch.observations, reduction="min")
        log_probs = self._policy.log_probs(batch.observations)
        probs = log_probs.exp()
        entropy = self._log_temp().exp() * log_probs
        return (probs * (entropy - q_t)).sum(dim=1).mean()

    @train_api
    def update_temp(self, batch: TorchMiniBatch) -> Tuple[float, float]:
        self._temp_optim.zero_grad()

        with torch.no_grad():
            log_probs = self._policy.log_probs(batch.observations)
            probs = log_probs.exp()
            expct_log_probs = (probs * log_probs).sum(dim=1, keepdim=True)
            entropy_target = 0.98 * (-math.log(1 / self.action_size))
            targ_temp = expct_log_probs + entropy_target

        loss = -(self._log_temp().exp() * targ_temp).mean()

        loss.backward()
        self._temp_optim.step()

        # current temperature value
        cur_temp = self._log_temp().exp().cpu().detach().numpy()[0][0]

        return float(loss.cpu().detach().numpy()), float(cur_temp)

    def inner_predict_best_action(self, x: torch.Tensor) -> torch.Tensor:
        return self._policy.best_action(x)

    def inner_sample_action(self, x: torch.Tensor) -> torch.Tensor:
        return self._policy.sample(x)

    def update_target(self) -> None:
        hard_sync(self._targ_q_func, self._q_func)

    @property
    def policy(self) -> Policy:
        return self._policy

    @property
    def policy_optim(self) -> Optimizer:
        return self._actor_optim

    @property
    def q_function(self) -> EnsembleQFunction:
        return self._q_func

    @property
    def q_function_optim(self) -> Optimizer:
        return self._critic_optim
