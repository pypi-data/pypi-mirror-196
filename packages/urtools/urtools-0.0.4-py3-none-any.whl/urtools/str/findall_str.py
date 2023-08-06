from __future__ import annotations
from typing import Iterable


def findall_str(text: str, substr: str) -> Iterable[int]:
    """Yields all the positions of the substring `substr` in the string `text`.

    Args
    ----------
    text : str
        Text in which we search for occurences of `substr`.

    substr : str
        A string for occurences of which we search in `text`.

    Yields
    ----------
    i : int
        Index of one occurence of `substr` in `text`.
    """

    i = text.find(substr)
    while i != -1:
        yield i
        i = text.find(substr, i + 1)
