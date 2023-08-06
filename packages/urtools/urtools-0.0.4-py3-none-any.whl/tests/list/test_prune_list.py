# pylint:disable=invalid-name,missing-function-docstring
import pytest


from urtools.list.prune_list import prune_list


@pytest.mark.parametrize(
    ("xs", "expected"),
    (
        ([1,2,1], [1,2]),
        ([], []),
        ([2,3,4,4,1,1,1,10], [2,3,4,1,10])
    ),
)
def test_prune_list(xs, expected):
    assert prune_list(xs) == expected
