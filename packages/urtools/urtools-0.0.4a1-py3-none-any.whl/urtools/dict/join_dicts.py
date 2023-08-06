def join_dicts(*dicts: dict) -> dict:
    """Join dictionaries into one.

    Note that "later" dicts override "earlier" ones.
    ```py
    join_dicts({1: 1, 2: 2}, {2: 3}) # {1: 1, 2: 3}
    ```
    """
    joined = {}
    for d in dicts:
        joined.update(d)
    return joined
