def has_nulls(xs: list) -> bool:
    """Check if this list contains any nulls"""
    return any(x is None or x != x for x in xs)
