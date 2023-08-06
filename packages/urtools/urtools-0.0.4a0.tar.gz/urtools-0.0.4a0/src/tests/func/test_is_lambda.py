# pylint:disable=wrong-import-position,wrong-import-order,ungrouped-imports,missing-function-docstring,unused-argument,invalid-name,multiple-statements
import logging
import math
import pytest

from urtools.func.is_lambda import is_lambda


@pytest.mark.parametrize("f", (print, logging.info, math.sqrt))
def test_neg(f):
    assert not is_lambda(f)


@pytest.mark.parametrize(
    "f", (lambda x: 1, lambda x: x**2, lambda xs: math.factorial(math.prod(xs)))
)
def test_pos(f):
    assert is_lambda(f)
