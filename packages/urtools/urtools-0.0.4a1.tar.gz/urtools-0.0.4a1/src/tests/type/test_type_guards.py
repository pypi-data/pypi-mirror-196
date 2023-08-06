# pylint:disable=invalid-name,missing-function-docstring
import numpy as np
import pytest

from urtools.type.type_guards import is_str, is_iter, is_str_or_non_iter, is_iter_and_non_str

@pytest.mark.parametrize(
    ("x", "expected"),
    (
        ("", True),
        (1, False),
        (None, False),
        ([""], False),
        (np.nan, False)
    )
)
def test_is_str(x, expected):
    assert is_str(x) == expected

@pytest.mark.parametrize(
    ("x", "expected"),
    (
        ("", True),
        (1, False),
        (None, False),
        ([""], True),
        (np.nan, False),
        ((x for x in range(10)), True),
        (tuple(range(10)), True),
        ((), True),
        ([], True),
        ({}, True),
        (set(), True)
    )
)
def test_is_iter(x, expected):
    assert is_iter(x) == expected
    
@pytest.mark.parametrize(
    ("x", "expected"),
    (
        ("", True),
        (1, True),
        (None, True),
        ([""], False),
        (np.nan, True),
        ((x for x in range(10)), False),
        (tuple(range(10)), False),
        ((), False),
        ([], False),
        ({}, False),
        (set(), False)
    )
)
def test_is_str_or_non_iter(x, expected):
    assert is_str_or_non_iter(x) == expected
    
@pytest.mark.parametrize(
    ("x", "expected"),
    (
        ("", False),
        (1, False),
        (None, False),
        ([""], True),
        (np.nan, False),
        ((x for x in range(10)), True),
        (tuple(range(10)), True),
        ((), True),
        ([], True),
        ({}, True),
        (set(), True)
    )
)
def test_is_iter_and_non_str(x, expected):
    assert is_iter_and_non_str(x) == expected
