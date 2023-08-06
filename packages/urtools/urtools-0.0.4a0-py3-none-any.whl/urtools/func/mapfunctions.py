from __future__ import annotations

from typing import Callable, Iterable, TypeVar
from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


def mapfunctions(
    functions: Iterable[Callable[P, R]], *args: P.args, **kwargs: P.kwargs
) -> list[R]:
    """Map an `Iterable` of functions to get a list of results."""
    return [f(*args, **kwargs) for f in functions]
