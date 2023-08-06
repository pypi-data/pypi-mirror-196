from __future__ import annotations

from typing import List, Iterable, Literal, Optional, TypeVar, overload


K = TypeVar("K")
V = TypeVar("V")
Keys = List[K]


def dict_multindex(
    d: dict[K, V],
    keys: Iterable[K],
) -> dict[K, V]:
    """Index dictionary using multiple keys"""
    return {key: d[key] for key in keys}


def dict_del_keys(d: dict[K, V], del_keys: Iterable[K]) -> dict[K, V]:
    """Get dictionary `d` but without keys in `del_keys`"""
    return {k: v for k, v in d.items() if k not in del_keys}


@overload
def dict_list_index(
    dict_list: Iterable[dict[K, V]],
    key: K,
    *,
    missing: Literal["nones"],
) -> list[Optional[V]]:
    ...


@overload
def dict_list_index(
    dict_list: Iterable[dict[K, V]],
    key: K,
    *,
    missing: Literal["skip", "error"] = "skip",
) -> list[V]:
    ...


def dict_list_index(
    dict_list: Iterable[dict[K, V]],
    key: K,
    *,
    missing: Literal["nones", "skip", "error"] = "skip",
) -> list[Optional[V]] | list[V]:
    """Take a list of dictionaries and index each one with the same key"""
    if missing == "nones":
        return [d.get(key) for d in dict_list]
    if missing == "skip":
        return [d[key] for d in dict_list if key in d]
    return [d[key] for d in dict_list]
