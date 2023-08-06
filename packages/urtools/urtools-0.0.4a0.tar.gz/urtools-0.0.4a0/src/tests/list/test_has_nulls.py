# pylint:disable=invalid-name,missing-function-docstring
import numpy as np
import pytest


from urtools.list.has_nulls import has_nulls


@pytest.mark.parametrize(
    ("xs", "expected"),
    (
        ([1, 2, np.nan], True),
        ([1, 2, 3], False),
        ([], False),
        ([None], True)
    ),
)
def test_batchsplit(xs, expected):
    assert has_nulls(xs) == expected
