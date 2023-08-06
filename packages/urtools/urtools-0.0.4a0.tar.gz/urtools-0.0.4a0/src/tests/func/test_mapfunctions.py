# pylint:disable=invalid-name,missing-function-docstring
import math
import pytest

from urtools.func.mapfunctions import mapfunctions


@pytest.mark.parametrize(
    ("fs", "x", "expected"),
    (
        ([math.sqrt, lambda x: x + 3], 9, [3, 12]),
        ([lambda x: math.pow(2, x), lambda x: math.pow(x, 2)], 3, [8, 9]),
    ),
)
def test_mapfunctions(fs, x, expected):
    assert mapfunctions(fs, x) == expected
