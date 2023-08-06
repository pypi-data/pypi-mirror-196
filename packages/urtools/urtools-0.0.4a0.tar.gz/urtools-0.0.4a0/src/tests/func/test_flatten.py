# pylint:disable=wrong-import-position,wrong-import-order,ungrouped-imports,missing-function-docstring,unused-argument,invalid-name,multiple-statements
import pytest

from urtools.func.flatten import flatten_l, flatten_s, flatten_t


@pytest.mark.parametrize(
    ("xs", "expected"),
    (
        (([1], ["b"], ["c"]), [1, "b", "c"]),
        ([[1], [], [1, 2]], [1, 1, 2]),
        ([], []),
        
    ),
)
def test_flatten_l(xs, expected):
    result = flatten_l(xs)
    assert result == expected

@pytest.mark.parametrize(
    ("xs", "expected"),
    (
        (((1, 2), (), (2, 3, 4)), (1, 2, 2, 3, 4)),
        ((), ()),
    ),
)
def test_flatten_t(xs, expected):
    result = flatten_t(xs)
    assert result == expected

@pytest.mark.parametrize(
    ("xs", "expected"),
    (
        (({1, 2}, set(), {2, 3, 4}), {1, 2, 3, 4}),
        (set(), set()),
    ),
)
def test_flatten_s(xs, expected):
    result = flatten_s(xs)
    assert result == expected
