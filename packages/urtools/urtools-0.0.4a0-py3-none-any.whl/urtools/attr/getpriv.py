from __future__ import annotations


def getpriv(x: object) -> list[str]:
    """Get all attributes of `x` that start with single underscore,
    i.e. are "private".
    """
    return [a for a in dir(x) if a.startswith("_") and not a.startswith("__")]
