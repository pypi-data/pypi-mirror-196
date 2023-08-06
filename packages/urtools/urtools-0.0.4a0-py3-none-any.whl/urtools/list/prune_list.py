from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def prune_list(xs: list[T]) -> list[T]:
    """Strip the list from repeating elements. 
    Preserves element ordering.
    """
    return list(dict.fromkeys(xs))
