from __future__ import annotations


def modify_str(
    old_str: str, new_substr: str, start: int, end: int | None = None
) -> str:
    """Modify a string by replacing a piece of it with a new substring
    or inserting a new substring.

    Args
    ----------
    old_str : str
        The string to be modified.
    new_substr : str
        A substring that will be inserted in the new string.
    start : int
        Position within `old_str` where `new_substr` insert starts.
    end : int | None, default=None
        Position within `old_str` where `new_substr` insert ends.
        If it is not `None`, must be greater than or equal to `start`.

    Note
    ----------
    If `end` is `None` (default value), then `new_substr` is just inserted into
    `old_str` at `start`-th position. If it is not `None`, then `new_substr` replaces
    the segment of `old_str` from `start` to `end`.
    """

    if end is None:
        end = start
    else:
        assert 0 <= start <= end, f"start must fall between 0 and {end=} but {start=}"
        assert end <= len(old_str), f"end must be smaller or equal than length of old_str but is {end=} whereas {len(old_str)=}"
    return old_str[:start] + new_substr + old_str[end:]
