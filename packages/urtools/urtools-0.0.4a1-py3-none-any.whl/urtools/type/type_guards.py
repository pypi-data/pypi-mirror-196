# pylint:disable=missing-function-docstring
from __future__ import annotations

from typing import Iterable

from typing_extensions import TypeGuard


def is_str(x: object) -> TypeGuard[str]:
    return isinstance(x, str)


def is_iter(x: object) -> TypeGuard[Iterable]:
    return isinstance(x, Iterable)


def is_str_or_non_iter(x: object) -> TypeGuard[str | Iterable]:
    """Is this a string OR not an iterable?"""
    return is_str(x) or not is_iter(x)


def is_iter_and_non_str(x: object) -> TypeGuard[Iterable]:
    """Is this an iterable AND not a string?"""
    return not is_str(x) and is_iter(x)
