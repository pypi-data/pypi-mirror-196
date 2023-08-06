# pylint:disable=wrong-import-position,wrong-import-order,ungrouped-imports,missing-function-docstring,unused-argument,invalid-name,multiple-statements

import pytest

from urtools.dict.join_dicts import join_dicts

d1 = {1: 1, 2: 2, 3: 3}
d2 = {2: 2, 3: 4, 10: 0}


@pytest.mark.parametrize(
    ("dicts", "expected"),
    (
        ([d1, d2], {1: 1, 2: 2, 3: 4, 10: 0}),
        ([d2, d1], {1: 1, 2: 2, 3: 3, 10: 0}),
        ([{}, {}], {}),
        ([{}, {1: 1}, {2: 2}], {1: 1, 2: 2}),
    ),
)
def test(dicts, expected):
    assert join_dicts(*dicts) == expected
