# pylint:disable=invalid-name,missing-function-docstring
import pytest

from urtools.list.batch_split import batch_split


@pytest.mark.parametrize(
    ("xs", "batch_size", "expected"),
    (
        (list(range(10)), 3, [[0,1,2], [3,4,5], [6,7,8], [9]]),
        (list(range(10)), 1, [[x] for x in range(10)]),
        ([], 1, []),
        ([], 100, [])
    ),
)
def test_batchsplit(xs, batch_size, expected):
    assert batch_split(xs, batch_size) == expected

def test_value_error():
    with pytest.raises(ValueError):
        batch_split([], -1)
        
def test_type_error():
    with pytest.raises(TypeError):
        batch_split([], 1.0)
        
