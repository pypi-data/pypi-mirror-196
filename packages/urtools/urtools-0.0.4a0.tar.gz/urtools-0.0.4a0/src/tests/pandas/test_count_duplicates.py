# pylint:disable=invalid-name,missing-function-docstring
import pandas as pd
import pytest

from urtools.pandas.count_duplicates import count_duplicates


iris = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')
    
@pytest.mark.parametrize(
    ("subset", "expected"),
    ( ("sepal_width", 127),
        ("sepal_length", 115),
        ("species", len(iris) - 3)
    )
)
def test_iris(subset, expected):
    assert count_duplicates(iris, subset) == expected

synth_data = pd.DataFrame([{"a": 1, "b": 2, "ccc": 333}, {"a": 1, "b": 22, "c": 3}])

@pytest.mark.parametrize(
    ("subset", "expected"),
    ( ("a", 1),
        ("b", 0),
        ("c", 0),
        (None, 0)
    )
)
def test_synth_data(subset, expected):
    assert count_duplicates(synth_data, subset) == expected

def test_synth_data_key_error():
    with pytest.raises(KeyError):
        count_duplicates(synth_data, "x")
