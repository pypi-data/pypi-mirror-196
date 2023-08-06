from __future__ import annotations

import pandas as pd

from urtools.dict.filter_dict_nans import filter_dict_nans


def df_to_jsonlist(df: pd.DataFrame, *, filter_nans: bool = True) -> list[dict]:
    """Convert a `DataFrame` into a list of rows as dicts.
    If you don't want to remove `nan` values from these dicts,
    specify `filter_nans=False`."""
    if filter_nans:
        return [filter_dict_nans(record) for record in df.to_dict(orient="records")]
    return df.to_dict(orient="records")
