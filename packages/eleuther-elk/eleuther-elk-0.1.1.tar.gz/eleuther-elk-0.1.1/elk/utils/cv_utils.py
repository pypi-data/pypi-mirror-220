from typing import Iterable, NamedTuple

import torch
from torch import Tensor


class LooFolds(NamedTuple):
    train: Tensor
    test: Tensor


def loo_folds(x: Tensor, dim: int = 0) -> Iterable[LooFolds]:
    """Efficiently create leave-one-out folds for cross-validation."""
    n = x.shape[dim]

    # Pad the tensor with a near-complete extra copy of itself
    # so that we can create a sliding window that wraps around
    padded = torch.cat([x, x.narrow(dim, 0, n - 1)], dim)
    windows = padded.unfold(dim, n, 1).movedim(-1, dim + 1)

    for window in windows.unbind(dim):
        yield LooFolds(
            # Train on all but the last element of each window
            train=window.narrow(dim, 0, n - 1),
            # Test on the last element of each window
            test=window.narrow(dim, n - 1, 1),
        )


def loo_mean(x: Tensor, dim: int = 0) -> Tensor:
    """Compute the leave-one-out means of `x` across `dim` in O(n) time."""
    n = x.shape[dim]
    assert n > 1, f"Dimension {dim} must have more than one element"

    # Compute the full sum, then subtract each element
    loo_sums = x.sum(dim=dim, keepdim=True) - x
    return loo_sums / (n - 1)
