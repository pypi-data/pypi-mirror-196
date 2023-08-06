# pylint:disable=invalid-name,missing-function-docstring
from collections import Counter
import numpy as np
import pandas as pd
import pytest

from urtools.pandas.df_to_jsonlist import df_to_jsonlist


iris = pd.read_csv(
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
)


def test_iris_filter_nans():
    jsonlist = df_to_jsonlist(iris, filter_nans=True)
    assert all(
        sorted(row)
        == ["petal_length", "petal_width", "sepal_length", "sepal_width", "species"]
        for row in jsonlist
    )


iris_null_virginica = iris.applymap(lambda x: np.nan if x == "virginica" else x)


def test_iris_null_virginica_filter_nans():
    jsonlist = df_to_jsonlist(iris_null_virginica, filter_nans=True)
    species_counts = Counter([r["species"] for r in jsonlist if "species" in r])
    assert (
        species_counts["setosa"] == 50
        and species_counts["versicolor"] == 50
        and np.nan not in species_counts
    )


def test_iris_null_virginica_dont_filter_nans():
    jsonlist = df_to_jsonlist(iris_null_virginica, filter_nans=False)
    species_counts = Counter([r["species"] for r in jsonlist])
    assert (
        species_counts["setosa"] == 50
        and species_counts["versicolor"] == 50
        and species_counts[np.nan] == 50
    )


def test_iris_null_virginica_filter_nans_error():
    jsonlist = df_to_jsonlist(iris_null_virginica, filter_nans=True)
    with pytest.raises(KeyError):
        Counter([r["species"] for r in jsonlist])
