#pylint:disable=wrong-import-position,wrong-import-order,ungrouped-imports,missing-function-docstring,unused-argument,invalid-name,multiple-statements

import numpy as np
import pytest

from urtools.dict import filter_dict_nans

@pytest.mark.parametrize(('d', 'expected'),
                         (
                             ({1: 1, 2: 2, 3: np.nan}, {1: 1, 2: 2}),
                             ({2: np.nan, 1: 2}, {1: 2}),
                             ({1: np.nan, "1": np.nan}, {})
                            )
                         )
def test_filtered_as_expected(d: dict, expected: dict):
    assert filter_dict_nans(d) == expected
