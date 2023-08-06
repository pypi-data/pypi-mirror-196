# pylint:disable=invalid-name,missing-function-docstring
import pytest

from urtools.str.findall_str import findall_str

@pytest.mark.parametrize(
    ("text", "substr", "expected"),
    (
        ("textrs", "t", [0, 3]),
        ("asdasdzczxc", "a", [0, 3]),
        ("asccxdasdzczxc", "c", [2, 3, 10, 13]),
        ("fooz barz, foozzzar fooz", "fooz", [0, 11, 20])
    )
)
def test(text, substr, expected):
    assert list(findall_str(text, substr)) == expected
