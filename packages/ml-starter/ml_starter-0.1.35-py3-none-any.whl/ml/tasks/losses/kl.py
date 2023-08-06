"""Defines KL-divergence utility functions."""

from torch import Tensor


def kl_single(mu: Tensor, log_var: Tensor, *, clamp_min: float = -30.0, clamp_max: float = 20.0) -> Tensor:
    log_var = log_var.clamp(min=clamp_min, max=clamp_max)
    var = log_var.exp()
    return -0.5 * (1 + log_var - mu.pow(2) - var)


def kl_pair(
    mu1: Tensor,
    log_var1: Tensor,
    mu2: Tensor,
    log_var2: Tensor,
    *,
    clamp_min: float = -30.0,
    clamp_max: float = 20.0,
) -> Tensor:
    log_var1 = log_var1.clamp(min=clamp_min, max=clamp_max)
    log_var2 = log_var2.clamp(min=clamp_min, max=clamp_max)
    var1 = log_var1.exp()
    var2 = log_var2.exp()
    return (log_var2 - log_var1) + (var1 + (mu1 - mu2).pow(2)) / var2 - 1
