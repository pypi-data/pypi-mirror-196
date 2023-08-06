from __future__ import annotations

import pandas as pd

from urtools.pandas.find_duplicates import find_duplicates


def count_duplicates(df: pd.DataFrame, subset: str | list[str] | None = None) -> int:
    """Count the number of duplicates in the `DataFrame`.
    `subset` specifies which columns of the `DataFrame` `df` to consider
    in order to identify duplicates. `None` means "use all columns".
    """
    return len(find_duplicates(df, subset))
