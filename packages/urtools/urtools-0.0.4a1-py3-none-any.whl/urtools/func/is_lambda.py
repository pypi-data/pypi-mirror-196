from typing import Callable


def is_lambda(func: Callable) -> bool:
    """Is `func` a nameless function?"""
    return "<lambda>" in str(func)
