import dataclasses
from typing import Dict

from ...base import DeviceArg, LearnableConfig, register_learnable
from ...constants import IMPL_NOT_INITIALIZED_ERROR, ActionSpace
from ...dataset import Shape
from ...models.builders import (
    create_conditional_vae,
    create_continuous_q_function,
    create_deterministic_residual_policy,
    create_discrete_imitator,
    create_discrete_q_function,
)
from ...models.encoders import EncoderFactory, make_encoder_field
from ...models.optimizers import OptimizerFactory, make_optimizer_field
from ...models.q_functions import QFunctionFactory, make_q_func_field
from ...models.torch import DiscreteImitator, PixelEncoder
from ...torch_utility import TorchMiniBatch
from .base import QLearningAlgoBase
from .torch.bcq_impl import BCQImpl, DiscreteBCQImpl

__all__ = ["BCQConfig", "BCQ", "DiscreteBCQConfig", "DiscreteBCQ"]


@dataclasses.dataclass()
class BCQConfig(LearnableConfig):
    r"""Config of Batch-Constrained Q-learning algorithm.

    BCQ is the very first practical data-driven deep reinforcement learning
    lgorithm.
    The major difference from DDPG is that the policy function is represented
    as combination of conditional VAE and perturbation function in order to
    remedy extrapolation error emerging from target value estimation.

    The encoder and the decoder of the conditional VAE is represented as
    :math:`E_\omega` and :math:`D_\omega` respectively.

    .. math::

        L(\omega) = E_{s_t, a_t \sim D} [(a - \tilde{a})^2
            + D_{KL}(N(\mu, \sigma)|N(0, 1))]

    where :math:`\mu, \sigma = E_\omega(s_t, a_t)`,
    :math:`\tilde{a} = D_\omega(s_t, z)` and :math:`z \sim N(\mu, \sigma)`.

    The policy function is represented as a residual function
    with the VAE and the perturbation function represented as
    :math:`\xi_\phi (s, a)`.

    .. math::

        \pi(s, a) = a + \Phi \xi_\phi (s, a)

    where :math:`a = D_\omega (s, z)`, :math:`z \sim N(0, 0.5)` and
    :math:`\Phi` is a perturbation scale designated by `action_flexibility`.
    Although the policy is learned closely to data distribution, the
    perturbation function can lead to more rewarded states.

    BCQ also leverages twin Q functions and computes weighted average over
    maximum values and minimum values.

    .. math::

        L(\theta_i) = \mathbb{E}_{s_t, a_t, r_{t+1}, s_{t+1} \sim D}
            [(y - Q_{\theta_i}(s_t, a_t))^2]

    .. math::

        y = r_{t+1} + \gamma \max_{a_i} [
            \lambda \min_j Q_{\theta_j'}(s_{t+1}, a_i)
            + (1 - \lambda) \max_j Q_{\theta_j'}(s_{t+1}, a_i)]

    where :math:`\{a_i \sim D(s_{t+1}, z), z \sim N(0, 0.5)\}_{i=1}^n`.
    The number of sampled actions is designated with `n_action_samples`.

    Finally, the perturbation function is trained just like DDPG's policy
    function.

    .. math::

        J(\phi) = \mathbb{E}_{s_t \sim D, a_t \sim D_\omega(s_t, z),
                              z \sim N(0, 0.5)}
            [Q_{\theta_1} (s_t, \pi(s_t, a_t))]

    At inference time, action candidates are sampled as many as
    `n_action_samples`, and the action with highest value estimation is taken.

    .. math::

        \pi'(s) = \text{argmax}_{\pi(s, a_i)} Q_{\theta_1} (s, \pi(s, a_i))

    Note:
        The greedy action is not deterministic because the action candidates
        are always randomly sampled. This might affect `save_policy` method and
        the performance at production.

    References:
        * `Fujimoto et al., Off-Policy Deep Reinforcement Learning without
          Exploration. <https://arxiv.org/abs/1812.02900>`_

    Args:
        observation_scaler (d3rlpy.preprocessing.ObservationScaler):
            Observation preprocessor.
        action_scaler (d3rlpy.preprocessing.ActionScaler): Action preprocessor.
        reward_scaler (d3rlpy.preprocessing.RewardScaler): Reward preprocessor.
        actor_learning_rate (float): Learning rate for policy function.
        critic_learning_rate (float): Learning rate for Q functions.
        imitator_learning_rate (float): Learning rate for Conditional VAE.
        actor_optim_factory (d3rlpy.models.optimizers.OptimizerFactory):
            Optimizer factory for the actor.
        critic_optim_factory (d3rlpy.models.optimizers.OptimizerFactory):
            Optimizer factory for the critic.
        imitator_optim_factory (d3rlpy.models.optimizers.OptimizerFactory):
            Optimizer factory for the conditional VAE.
        actor_encoder_factory (d3rlpy.models.encoders.EncoderFactory):
            Encoder factory for the actor.
        critic_encoder_factory (d3rlpy.models.encoders.EncoderFactory):
            Encoder factory for the critic.
        imitator_encoder_factory (d3rlpy.models.encoders.EncoderFactory):
            Encoder factory for the conditional VAE.
        q_func_factory (d3rlpy.models.q_functions.QFunctionFactory):
            Q function factory.
        batch_size (int): Mini-batch size.
        gamma (float): Discount factor.
        tau (float): Target network synchronization coefficiency.
        n_critics (int): Number of Q functions for ensemble.
        update_actor_interval (int): Interval to update policy function.
        lam (float): Weight factor for critic ensemble.
        n_action_samples (int): Number of action samples to estimate
            action-values.
        action_flexibility (float): Output scale of perturbation function
            represented as :math:`\Phi`.
        rl_start_step (int): Steps to start to update policy function and Q
            functions. If this is large, RL training would be more stabilized.
        beta (float): KL reguralization term for Conditional VAE.
    """
    actor_learning_rate: float = 1e-3
    critic_learning_rate: float = 1e-3
    imitator_learning_rate: float = 1e-3
    actor_optim_factory: OptimizerFactory = make_optimizer_field()
    critic_optim_factory: OptimizerFactory = make_optimizer_field()
    imitator_optim_factory: OptimizerFactory = make_optimizer_field()
    actor_encoder_factory: EncoderFactory = make_encoder_field()
    critic_encoder_factory: EncoderFactory = make_encoder_field()
    imitator_encoder_factory: EncoderFactory = make_encoder_field()
    q_func_factory: QFunctionFactory = make_q_func_field()
    batch_size: int = 100
    gamma: float = 0.99
    tau: float = 0.005
    n_critics: int = 2
    update_actor_interval: int = 1
    lam: float = 0.75
    n_action_samples: int = 100
    action_flexibility: float = 0.05
    rl_start_step: int = 0
    beta: float = 0.5

    def create(self, device: DeviceArg = False) -> "BCQ":
        return BCQ(self, device)

    @staticmethod
    def get_type() -> str:
        return "bcq"


class BCQ(QLearningAlgoBase[BCQImpl, BCQConfig]):
    def inner_create_impl(
        self, observation_shape: Shape, action_size: int
    ) -> None:
        policy = create_deterministic_residual_policy(
            observation_shape,
            action_size,
            self._config.action_flexibility,
            self._config.actor_encoder_factory,
            device=self._device,
        )
        q_func = create_continuous_q_function(
            observation_shape,
            action_size,
            self._config.critic_encoder_factory,
            self._config.q_func_factory,
            n_ensembles=self._config.n_critics,
            device=self._device,
        )
        imitator = create_conditional_vae(
            observation_shape=observation_shape,
            action_size=action_size,
            latent_size=2 * action_size,
            beta=self._config.beta,
            min_logstd=-4.0,
            max_logstd=15.0,
            encoder_factory=self._config.imitator_encoder_factory,
            device=self._device,
        )

        actor_optim = self._config.actor_optim_factory.create(
            policy.parameters(), lr=self._config.actor_learning_rate
        )
        critic_optim = self._config.critic_optim_factory.create(
            q_func.parameters(), lr=self._config.critic_learning_rate
        )
        imitator_optim = self._config.imitator_optim_factory.create(
            imitator.parameters(), lr=self._config.imitator_learning_rate
        )

        self._impl = BCQImpl(
            observation_shape=observation_shape,
            action_size=action_size,
            policy=policy,
            q_func=q_func,
            imitator=imitator,
            actor_optim=actor_optim,
            critic_optim=critic_optim,
            imitator_optim=imitator_optim,
            gamma=self._config.gamma,
            tau=self._config.tau,
            lam=self._config.lam,
            n_action_samples=self._config.n_action_samples,
            action_flexibility=self._config.action_flexibility,
            beta=self._config.beta,
            device=self._device,
        )

    def inner_update(self, batch: TorchMiniBatch) -> Dict[str, float]:
        assert self._impl is not None, IMPL_NOT_INITIALIZED_ERROR

        metrics = {}

        imitator_loss = self._impl.update_imitator(batch)
        metrics.update({"imitator_loss": imitator_loss})

        if self._grad_step >= self._config.rl_start_step:
            critic_loss = self._impl.update_critic(batch)
            metrics.update({"critic_loss": critic_loss})

            if self._grad_step % self._config.update_actor_interval == 0:
                actor_loss = self._impl.update_actor(batch)
                metrics.update({"actor_loss": actor_loss})
                self._impl.update_actor_target()
                self._impl.update_critic_target()

        return metrics

    def get_action_type(self) -> ActionSpace:
        return ActionSpace.CONTINUOUS


@dataclasses.dataclass()
class DiscreteBCQConfig(LearnableConfig):
    r"""Config of Discrete version of Batch-Constrained Q-learning algorithm.

    Discrete version takes theories from the continuous version, but the
    algorithm is much simpler than that.
    The imitation function :math:`G_\omega(a|s)` is trained as supervised
    learning just like Behavior Cloning.

    .. math::

        L(\omega) = \mathbb{E}_{a_t, s_t \sim D}
            [-\sum_a p(a|s_t) \log G_\omega(a|s_t)]

    With this imitation function, the greedy policy is defined as follows.

    .. math::

        \pi(s_t) = \text{argmax}_{a|G_\omega(a|s_t)
                / \max_{\tilde{a}} G_\omega(\tilde{a}|s_t) > \tau}
            Q_\theta (s_t, a)

    which eliminates actions with probabilities :math:`\tau` times smaller
    than the maximum one.

    Finally, the loss function is computed in Double DQN style with the above
    constrained policy.

    .. math::

        L(\theta) = \mathbb{E}_{s_t, a_t, r_{t+1}, s_{t+1} \sim D} [(r_{t+1}
            + \gamma Q_{\theta'}(s_{t+1}, \pi(s_{t+1}))
            - Q_\theta(s_t, a_t))^2]

    References:
        * `Fujimoto et al., Off-Policy Deep Reinforcement Learning without
          Exploration. <https://arxiv.org/abs/1812.02900>`_
        * `Fujimoto et al., Benchmarking Batch Deep Reinforcement Learning
          Algorithms. <https://arxiv.org/abs/1910.01708>`_

    Args:
        observation_scaler (d3rlpy.preprocessing.ObservationScaler):
            Observation preprocessor.
        reward_scaler (d3rlpy.preprocessing.RewardScaler): Reward preprocessor.
        learning_rate (float): Learning rate.
        optim_factory (d3rlpy.models.optimizers.OptimizerFactory):
            Optimizer factory.
        encoder_factory (d3rlpy.models.encoders.EncoderFactory or str):
            Encoder factory.
        q_func_factory (d3rlpy.models.q_functions.QFunctionFactory or str):
            Q function factory.
        batch_size (int): Mini-batch size.
        gamma (float): Discount factor.
        n_critics (int): Number of Q functions for ensemble.
        action_flexibility (float): Probability threshold represented as
            :math:`\tau`.
        beta (float): Reguralization term for imitation function.
        target_update_interval (int): Interval to update the target network.
    """
    learning_rate: float = 6.25e-5
    optim_factory: OptimizerFactory = make_optimizer_field()
    encoder_factory: EncoderFactory = make_encoder_field()
    q_func_factory: QFunctionFactory = make_q_func_field()
    batch_size: int = 32
    gamma: float = 0.99
    n_critics: int = 1
    action_flexibility: float = 0.3
    beta: float = 0.5
    target_update_interval: int = 8000

    def create(self, device: DeviceArg = False) -> "DiscreteBCQ":
        return DiscreteBCQ(self, device)

    @staticmethod
    def get_type() -> str:
        return "discrete_bcq"


class DiscreteBCQ(QLearningAlgoBase[DiscreteBCQImpl, DiscreteBCQConfig]):
    def inner_create_impl(
        self, observation_shape: Shape, action_size: int
    ) -> None:
        q_func = create_discrete_q_function(
            observation_shape,
            action_size,
            self._config.encoder_factory,
            self._config.q_func_factory,
            n_ensembles=self._config.n_critics,
            device=self._device,
        )

        # share convolutional layers if observation is pixel
        if isinstance(q_func.q_funcs[0].encoder, PixelEncoder):
            imitator = DiscreteImitator(
                q_func.q_funcs[0].encoder, action_size, self._config.beta
            )
            imitator.to(self._device)
        else:
            imitator = create_discrete_imitator(
                observation_shape,
                action_size,
                self._config.beta,
                self._config.encoder_factory,
                device=self._device,
            )

        # TODO: replace this with a cleaner way
        # retrieve unique elements
        q_func_params = list(q_func.parameters())
        imitator_params = list(imitator.parameters())
        unique_dict = {}
        for param in q_func_params + imitator_params:
            unique_dict[param] = param
        unique_params = list(unique_dict.values())
        optim = self._config.optim_factory.create(
            unique_params, lr=self._config.learning_rate
        )

        self._impl = DiscreteBCQImpl(
            observation_shape=observation_shape,
            action_size=action_size,
            q_func=q_func,
            imitator=imitator,
            optim=optim,
            gamma=self._config.gamma,
            action_flexibility=self._config.action_flexibility,
            beta=self._config.beta,
            device=self._device,
        )

    def inner_update(self, batch: TorchMiniBatch) -> Dict[str, float]:
        assert self._impl is not None, IMPL_NOT_INITIALIZED_ERROR
        loss = self._impl.update(batch)
        if self._grad_step % self._config.target_update_interval == 0:
            self._impl.update_target()
        return {"loss": loss}

    def get_action_type(self) -> ActionSpace:
        return ActionSpace.DISCRETE


register_learnable(BCQConfig)
register_learnable(DiscreteBCQConfig)
