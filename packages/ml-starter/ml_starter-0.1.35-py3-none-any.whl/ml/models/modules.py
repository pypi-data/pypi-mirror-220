"""Miscellaneous shared modules which can be used in various models."""

from torch import Tensor
from torch.autograd.function import Function, FunctionCtx


class _InvertGrad(Function):
    @staticmethod
    def forward(ctx: FunctionCtx, input: Tensor, scale: float) -> Tensor:  # type: ignore[override]
        ctx.scale = scale
        return input

    @staticmethod
    def backward(ctx: FunctionCtx, grad_output: Tensor) -> Tensor:  # type: ignore[override]
        return grad_output * ctx.scale


def scale_grad(input: Tensor, scale: float) -> Tensor:
    """Scales the gradient of the input.

    Args:
        input: Input tensor.
        scale: Scale factor.

    Returns:
        The identity of the input tensor in the forward pass, and the scaled
        gradient in the backward pass.
    """
    return _InvertGrad.apply(input)


def invert_grad(input: Tensor) -> Tensor:
    return scale_grad(input, -1.0)
