from typing import Sequence, cast

import torch
from torch import nn

from ..dataset import Shape
from .encoders import EncoderFactory
from .q_functions import QFunctionFactory
from .torch import (
    CategoricalPolicy,
    ConditionalVAE,
    ContinuousDecisionTransformer,
    DeterministicPolicy,
    DeterministicRegressor,
    DeterministicResidualPolicy,
    DiscreteDecisionTransformer,
    DiscreteImitator,
    EnsembleContinuousQFunction,
    EnsembleDiscreteQFunction,
    GlobalPositionEncoding,
    NonSquashedNormalPolicy,
    Parameter,
    ProbablisticRegressor,
    SimplePositionEncoding,
    SquashedNormalPolicy,
    ValueFunction,
)
from .utility import create_activation

__all__ = [
    "create_discrete_q_function",
    "create_continuous_q_function",
    "create_deterministic_policy",
    "create_deterministic_residual_policy",
    "create_squashed_normal_policy",
    "create_non_squashed_normal_policy",
    "create_categorical_policy",
    "create_conditional_vae",
    "create_discrete_imitator",
    "create_deterministic_regressor",
    "create_probablistic_regressor",
    "create_value_function",
    "create_parameter",
    "create_continuous_decision_transformer",
    "create_discrete_decision_transformer",
]


def create_discrete_q_function(
    observation_shape: Shape,
    action_size: int,
    encoder_factory: EncoderFactory,
    q_func_factory: QFunctionFactory,
    device: str,
    n_ensembles: int = 1,
) -> EnsembleDiscreteQFunction:
    if q_func_factory.share_encoder:
        encoder = encoder_factory.create(observation_shape)
        # normalize gradient scale by ensemble size
        for p in cast(nn.Module, encoder).parameters():
            p.register_hook(lambda grad: grad / n_ensembles)

    q_funcs = []
    for _ in range(n_ensembles):
        if not q_func_factory.share_encoder:
            encoder = encoder_factory.create(observation_shape)
        q_funcs.append(q_func_factory.create_discrete(encoder, action_size))
    q_func = EnsembleDiscreteQFunction(q_funcs)
    q_func.to(device)
    return q_func


def create_continuous_q_function(
    observation_shape: Shape,
    action_size: int,
    encoder_factory: EncoderFactory,
    q_func_factory: QFunctionFactory,
    device: str,
    n_ensembles: int = 1,
) -> EnsembleContinuousQFunction:
    if q_func_factory.share_encoder:
        encoder = encoder_factory.create_with_action(
            observation_shape, action_size
        )
        # normalize gradient scale by ensemble size
        for p in cast(nn.Module, encoder).parameters():
            p.register_hook(lambda grad: grad / n_ensembles)

    q_funcs = []
    for _ in range(n_ensembles):
        if not q_func_factory.share_encoder:
            encoder = encoder_factory.create_with_action(
                observation_shape, action_size
            )
        q_funcs.append(q_func_factory.create_continuous(encoder))
    q_func = EnsembleContinuousQFunction(q_funcs)
    q_func.to(device)
    return q_func


def create_deterministic_policy(
    observation_shape: Shape,
    action_size: int,
    encoder_factory: EncoderFactory,
    device: str,
) -> DeterministicPolicy:
    encoder = encoder_factory.create(observation_shape)
    policy = DeterministicPolicy(encoder, action_size)
    policy.to(device)
    return policy


def create_deterministic_residual_policy(
    observation_shape: Shape,
    action_size: int,
    scale: float,
    encoder_factory: EncoderFactory,
    device: str,
) -> DeterministicResidualPolicy:
    encoder = encoder_factory.create_with_action(observation_shape, action_size)
    policy = DeterministicResidualPolicy(encoder, scale)
    policy.to(device)
    return policy


def create_squashed_normal_policy(
    observation_shape: Shape,
    action_size: int,
    encoder_factory: EncoderFactory,
    device: str,
    min_logstd: float = -20.0,
    max_logstd: float = 2.0,
    use_std_parameter: bool = False,
) -> SquashedNormalPolicy:
    encoder = encoder_factory.create(observation_shape)
    policy = SquashedNormalPolicy(
        encoder,
        action_size,
        min_logstd=min_logstd,
        max_logstd=max_logstd,
        use_std_parameter=use_std_parameter,
    )
    policy.to(device)
    return policy


def create_non_squashed_normal_policy(
    observation_shape: Shape,
    action_size: int,
    encoder_factory: EncoderFactory,
    device: str,
    min_logstd: float = -20.0,
    max_logstd: float = 2.0,
    use_std_parameter: bool = False,
) -> NonSquashedNormalPolicy:
    encoder = encoder_factory.create(observation_shape)
    policy = NonSquashedNormalPolicy(
        encoder,
        action_size,
        min_logstd=min_logstd,
        max_logstd=max_logstd,
        use_std_parameter=use_std_parameter,
    )
    policy.to(device)
    return policy


def create_categorical_policy(
    observation_shape: Shape,
    action_size: int,
    encoder_factory: EncoderFactory,
    device: str,
) -> CategoricalPolicy:
    encoder = encoder_factory.create(observation_shape)
    policy = CategoricalPolicy(encoder, action_size)
    policy.to(device)
    return policy


def create_conditional_vae(
    observation_shape: Shape,
    action_size: int,
    latent_size: int,
    beta: float,
    encoder_factory: EncoderFactory,
    device: str,
    min_logstd: float = -20.0,
    max_logstd: float = 2.0,
) -> ConditionalVAE:
    encoder_encoder = encoder_factory.create_with_action(
        observation_shape, action_size
    )
    decoder_encoder = encoder_factory.create_with_action(
        observation_shape, latent_size
    )
    policy = ConditionalVAE(
        encoder_encoder,
        decoder_encoder,
        beta,
        min_logstd=min_logstd,
        max_logstd=max_logstd,
    )
    policy.to(device)
    return policy


def create_discrete_imitator(
    observation_shape: Shape,
    action_size: int,
    beta: float,
    encoder_factory: EncoderFactory,
    device: str,
) -> DiscreteImitator:
    encoder = encoder_factory.create(observation_shape)
    imitator = DiscreteImitator(encoder, action_size, beta)
    imitator.to(device)
    return imitator


def create_deterministic_regressor(
    observation_shape: Shape,
    action_size: int,
    encoder_factory: EncoderFactory,
    device: str,
) -> DeterministicRegressor:
    encoder = encoder_factory.create(observation_shape)
    regressor = DeterministicRegressor(encoder, action_size)
    regressor.to(device)
    return regressor


def create_probablistic_regressor(
    observation_shape: Shape,
    action_size: int,
    encoder_factory: EncoderFactory,
    device: str,
    min_logstd: float = -20.0,
    max_logstd: float = 2.0,
) -> ProbablisticRegressor:
    encoder = encoder_factory.create(observation_shape)
    regressor = ProbablisticRegressor(
        encoder, action_size, min_logstd=min_logstd, max_logstd=max_logstd
    )
    regressor.to(device)
    return regressor


def create_value_function(
    observation_shape: Shape, encoder_factory: EncoderFactory, device: str
) -> ValueFunction:
    encoder = encoder_factory.create(observation_shape)
    value_func = ValueFunction(encoder)
    value_func.to(device)
    return value_func


def create_parameter(
    shape: Sequence[int], initial_value: float, device: str
) -> Parameter:
    data = torch.full(shape, initial_value, dtype=torch.float32)
    parameter = Parameter(data)
    parameter.to(device)
    return parameter


def create_continuous_decision_transformer(
    observation_shape: Shape,
    action_size: int,
    encoder_factory: EncoderFactory,
    num_heads: int,
    max_timestep: int,
    num_layers: int,
    context_size: int,
    attn_dropout: float,
    resid_dropout: float,
    embed_dropout: float,
    activation_type: str,
    position_encoding_type: str,
    device: str,
) -> ContinuousDecisionTransformer:
    encoder = encoder_factory.create(observation_shape)
    hidden_size = encoder.get_feature_size()

    if position_encoding_type == "simple":
        position_encoding = SimplePositionEncoding(hidden_size, max_timestep)
    elif position_encoding_type == "global":
        position_encoding = GlobalPositionEncoding(
            hidden_size, max_timestep, context_size
        )
    else:
        raise ValueError(
            f"invalid position_encoding_type: {position_encoding_type}"
        )

    transformer = ContinuousDecisionTransformer(
        encoder=encoder,
        position_encoding=position_encoding,
        action_size=action_size,
        num_heads=num_heads,
        context_size=context_size,
        num_layers=num_layers,
        attn_dropout=attn_dropout,
        resid_dropout=resid_dropout,
        embed_dropout=embed_dropout,
        activation=create_activation(activation_type),
    )
    transformer.to(device)
    return transformer


def create_discrete_decision_transformer(
    observation_shape: Shape,
    action_size: int,
    encoder_factory: EncoderFactory,
    num_heads: int,
    max_timestep: int,
    num_layers: int,
    context_size: int,
    attn_dropout: float,
    resid_dropout: float,
    embed_dropout: float,
    activation_type: str,
    position_encoding_type: str,
    device: str,
) -> DiscreteDecisionTransformer:
    encoder = encoder_factory.create(observation_shape)
    hidden_size = encoder.get_feature_size()

    if position_encoding_type == "simple":
        position_encoding = SimplePositionEncoding(hidden_size, max_timestep)
    elif position_encoding_type == "global":
        position_encoding = GlobalPositionEncoding(
            hidden_size, max_timestep, context_size
        )
    else:
        raise ValueError(
            f"invalid position_encoding_type: {position_encoding_type}"
        )

    transformer = DiscreteDecisionTransformer(
        encoder=encoder,
        position_encoding=position_encoding,
        action_size=action_size,
        num_heads=num_heads,
        context_size=context_size,
        num_layers=num_layers,
        attn_dropout=attn_dropout,
        resid_dropout=resid_dropout,
        embed_dropout=embed_dropout,
        activation=create_activation(activation_type),
    )
    transformer.to(device)
    return transformer
