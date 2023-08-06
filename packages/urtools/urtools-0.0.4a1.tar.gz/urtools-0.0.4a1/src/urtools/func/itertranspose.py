from __future__ import annotations

from functools import reduce
from typing import Any, Callable, Iterable, TypeVar, Union, cast

T = TypeVar("T")
Applicative = Union[str, Callable[[T], Any]]
Filter = Callable[[T], bool]


def itertranspose(
    it: Iterable[T],
    /,
    applicatives: Applicative | Iterable[Applicative],
    filters: Filter | Iterable[Filter] = (),
) -> tuple[list, ...]:
    """Process an iterable into a tuple of lists, each containing results of processing each element
    with one of `applicatives` iff it has passed through all `filters`.

    Args
    ----------
    it : Iterable[T]
        An iterable to be processed.
    applicatives:
        Attributes (strings) or callables (functions) that are supposed to be used in processing
        the elements of `it` that have passed through all `filters`.
    filters:
        One-argument bool-returning functions that are applied to every element of `it`.
        Iff each filter returns `True` the element is being passed to each applicative
        and results are aggregated into separate lists, one per each attribute.
    """
    # Validate args
    # it
    if isinstance(it, Iterable):
        it = tuple(it)
    elif not isinstance(it, Iterable):
        raise ValueError(f"`it` should be an iterable but is {type(it)}")
    # applicatives
    if isinstance(applicatives, Iterable):
        applicatives = tuple(applicatives)
    elif isinstance(applicatives, (str, Callable)):
        applicatives = (applicatives,)
    if not all(isinstance(a, (str, Callable)) for a in applicatives):
        raise ValueError(
            f"`applicatives` should be a string (attribute name) or a one-argument "
            f"callable (or a list thereof):\n{applicatives=}"
        )
    # filters
    if isinstance(filters, Iterable):
        filters = tuple(filters)
    elif isinstance(filters, Callable):
        filters = (filters,)
    if not all(isinstance(f, Callable) for f in filters):
        raise ValueError(
            f"`filters` should be one-argument callables:\n{applicatives=}"
        )

    # Define the function
    def func(initial: tuple[list, ...], x) -> tuple[list, ...]:
        return tuple(
            [*initial[i], _apply(x, app)]
            if all(f(x) for f in cast(tuple, filters))
            else initial[i]
            for i, app in enumerate(cast(tuple, applicatives))
        )

    # Initialize starting value to a tuple of lists.
    # The size depends on how many attributes we want to extract from each element of `it`.
    initial: tuple[list, ...] = len(applicatives) * ([],)

    return reduce(func, it, initial)


R = TypeVar("R")


def _apply(x: T, applicative: str | Callable[[T], R]) -> R:
    if isinstance(applicative, str):
        return getattr(x, applicative)
    return applicative(x)
