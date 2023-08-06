from __future__ import annotations

from inspect import getfullargspec
from typing import Callable, Generic, Hashable, TypeVar, Union, cast

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")
CallbackArgType = Union[Callable[[K], V], Callable[[], V], V, None]

T = TypeVar("T")


def _identity(x: T, /) -> T:
    """Identity function. Returns whatever it was given."""
    return x


class CallbackDict(dict, Generic[K, V]):
    """A dictionary with an optional callback, i.e. a function that
    specifies what should be returned if a key wasn't found in the dictionary.
    """

    __slots__ = ("callback",)
    callback: Callable[[K], V]

    def __init__(self, callback: CallbackArgType = None, /, **rest) -> None:
        if callback is None:
            self.callback = cast(Callable[[K], V], _identity)
        elif isinstance(callback, Callable):
            if (callback_n_args := len(getfullargspec(callback).args)) > 1:
                raise AttributeError(
                    f"Callback should take 1 or 0 arguments, takes {callback_n_args}"
                )
            if callback_n_args == 1:
                self.callback = cast(Callable[[K], V], callback)
            else:
                self.callback = lambda k: cast(Callable[[], V], callback)()
        else:
            self.callback = lambda k: cast(V, callback)
        super().__init__(**rest)

    def __getitem__(self, k: K) -> V:
        if k in self:
            return super().__getitem__(k)
        return self.callback(k)

    def __setitem__(self, k: K, v: V) -> None:
        return super().__setitem__(k, v)
