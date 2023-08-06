# pylint:disable=invalid-name,missing-function-docstring
import pytest

from urtools.str.partition_n import partition_n

@pytest.mark.parametrize(
    ("string", "sep", "n", "expected"),
    (
        ("abc abc", "c", None, ["ab", "c", " ab", "c"]),
        ("123|abc|zxczx|||", "|", None, ["123","|","abc","|","zxczx","|","|","|"]),
        ("", "x", None, []),
        (" ", "x", None, [" "]),
        ("abc", "||", None, ["abc"]),
        ("a|b|c", "|", 1, ["a", "|", "b|c"]),
        ("a|b|c", "|", 0, ["a|b|c"]),
    )
)
def test_partition_n(string, sep, n, expected):
    assert partition_n(string, sep, n) == expected
