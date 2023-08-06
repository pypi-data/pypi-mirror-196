# pylint:disable=wrong-import-position,wrong-import-order,ungrouped-imports,missing-function-docstring,unused-argument,invalid-name,multiple-statements

import pytest

from urtools.dict.is_subdict import is_subdict


@pytest.mark.parametrize(
    ("sub_dict", "sup_dict", "expected"),
    (
        ({1: 1}, {2: 2, 1: 1}, True),
        ({}, {1: 1}, True),
        ({1: 1}, {}, False),
        ({}, {}, True),
        ({1: 1}, {2: 2}, False),
        ({1: 1, 2: 2}, {1: 1, 0: 0}, False),
        ({1: 1}, {1: 2, 2: 2}, False),
    ),
)
def test(sub_dict, sup_dict, expected):
    assert is_subdict(sub_dict, sup_dict) == expected
