# pylint:disable=invalid-name,missing-function-docstring
import pytest

from urtools.str.modify_str import modify_str

@pytest.mark.parametrize(
    ("old_str", "new_substr", "start","end","expected"),
    (
        ("aabbcc", "zx", 2, 4, "aazxcc"),
        ("abcdef", "fedcba", 0, 6, "fedcba"),
        ("1234", "", 0, 4, ""),
        ("", "123", 0, 0, "123")
    )
)
def test_with_end_specified(old_str, new_substr, start, end, expected):
    assert modify_str(old_str, new_substr, start, end) == expected

@pytest.mark.parametrize(
    ("old_str", "new_substr", "start","expected"),
    (
        ("aabbcc", "zx", 2, "aazxbbcc"),
        ("abcdef", "fedcba", 0, "fedcbaabcdef"),
        ("1234", "", 0, "1234"),
        ("", "123", 0,  "123")
    )
)
def test_with_end_unspecified(old_str, new_substr, start, expected):
    assert modify_str(old_str, new_substr, start) == expected

@pytest.mark.parametrize(
    ("old_str", "new_substr", "start","end","expected"),
    (
        ("aabbcc", "zx", -1, 4, "aazxcc"),
        ("abcdef", "fedcba", 0, 100, "fedcba"),
    )
)
def test_assertion_error(old_str, new_substr, start, end, expected):
    with pytest.raises(AssertionError):
        modify_str(old_str, new_substr, start, end) == expected
