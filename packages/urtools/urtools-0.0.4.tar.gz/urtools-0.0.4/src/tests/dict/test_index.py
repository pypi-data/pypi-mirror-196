# pylint:disable=wrong-import-position,wrong-import-order,ungrouped-imports,missing-function-docstring,unused-argument,invalid-name,multiple-statements,missing-class-docstring
import logging

LOGGER = logging.getLogger(__name__)

import pytest


from urtools.dict.index import dict_multindex


class Test_dict_multindex:
    d_1 = {1: 1, 2: 2, "key": "KEY"}

    @pytest.mark.parametrize(
        ("keys", "expected"),
        ((["key"], {"key": "KEY"}), ([1, 2], {1: 1, 2: 2}), (d_1.keys(), d_1)),
    )
    def test_keys(self, keys, expected: dict):
        result = dict_multindex(self.d_1, keys=keys)
        assert result == expected


from urtools.dict.index import dict_del_keys


class Test_dict_del_keys:
    d_1 = {1: 1, 2: 2, "a": "a", "bb": "bb"}

    @pytest.mark.parametrize(
        ("del_keys", "expected"),
        (
            ([1], {2: 2, "a": "a", "bb": "bb"}),
            (d_1.keys(), {}),
            (list(d_1.keys()) + [3, 4, 5], {}),
            ([], d_1),
        ),
    )
    def test(self, del_keys, expected):
        res = dict_del_keys(self.d_1, del_keys)
        assert res == expected


from urtools.dict.index import dict_list_index


class Test_dict_list_index:
    dl_1 = [{1: 2}, {1: 3}, {2: 2}]

    @pytest.mark.parametrize(
        ("key", "expected"),
        ((1, [2, 3, None]), (2, [None, None, 2]), ("x", 3 * [None])),
    )
    def test_missing_nones(self, key, expected):
        result = dict_list_index(self.dl_1, key, missing="nones")
        assert result == expected

    @pytest.mark.parametrize(
        ("key", "expected"),
        ((1, [2, 3]), (2, [2]), ("x", [])),
    )
    def test_missing_skip(self, key, expected):
        result = dict_list_index(self.dl_1, key, missing="skip")
        assert result == expected

    def test_missing_no_error(self):
        result = dict_list_index([{1: 1, "1": "1"}, {1: 2, 2: 10}], 1, missing="error")
        assert result == [1, 2]

    @pytest.mark.parametrize(
        ("key"),
        (1, 2, "x"),
    )
    def test_missing_error(self, key):
        with pytest.raises(KeyError):
            result = dict_list_index(self.dl_1, key, missing="error")
