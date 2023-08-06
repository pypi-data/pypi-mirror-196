from __future__ import annotations

import pandas as pd


def find_duplicates(df: pd.DataFrame, subset: str | list[str] | None = None) -> list:
    """Return indices of rows that are duplicates of other rows.
    `subset` specifies which columns of the `DataFrame` `df` to consider
    in order to identify duplicates. `None` means "use all columns".
    """
    df_post_drop = df.drop_duplicates(subset=subset)
    dropped_inds = sorted(
        set(df.index.tolist()).difference(df_post_drop.index.tolist())
    )
    return dropped_inds
