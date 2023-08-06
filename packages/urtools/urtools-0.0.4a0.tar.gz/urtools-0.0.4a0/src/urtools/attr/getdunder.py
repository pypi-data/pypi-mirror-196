from __future__ import annotations


def getdunder(x: object) -> list[str]:
    """Get all dunder attributes of `x`"""
    return [a for a in dir(x) if a.startswith("__") and a.endswith("__")]
