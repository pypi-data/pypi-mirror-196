from __future__ import annotations

from typing import TypeVar

V = TypeVar("V")


def json_keys2int(d: dict[str, V]) -> dict[str | int, V]:
    """A util to convert json objects' keys from strings to ints (where they should be ints)"""
    if isinstance(d, dict):
        assert all(str(k).isdigit() and float(k) == int(k) for k in d)
        return {int(k): v for k, v in d.items()}
    return d
