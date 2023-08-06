from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def batch_split(xs: list[T], batch_size: int) -> list[list[T]]:
    """Split the list into a number of batches (smaller lists)."""
    if not isinstance(batch_size, int):
        raise TypeError(f"batch_size must be positive integer, not {batch_size} of type {type(batch_size)}")
    if batch_size <= 0:
        raise ValueError(f"batch_size must be positive integer, not {batch_size}")
    return [
        xs[i * batch_size : (i + 1) * batch_size]
        for i in range((len(xs) // batch_size) + 1) if i < len(xs)
    ]
