from __future__ import annotations

from functools import reduce
from operator import add, or_
from typing import Iterable, TypeVar


T = TypeVar("T")


def flatten_l(xs: Iterable[list[T]]) -> list[T]:
    """Join lists of the same inner type into one list"""
    return reduce(add, xs, [])


def flatten_s(xs: Iterable[set[T]]) -> set[T]:
    """Join set of the same inner type into one set"""
    return reduce(or_, xs, set())


def flatten_t(xs: Iterable[tuple[T, ...]]) -> tuple[T, ...]:
    """Join tuples of the same inner type into one tuple"""
    return reduce(add, xs, ())
