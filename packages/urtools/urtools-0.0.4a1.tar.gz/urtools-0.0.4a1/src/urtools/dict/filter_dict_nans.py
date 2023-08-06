def filter_dict_nans(d: dict) -> dict:
    """Remove nan values from dictionary"""
    return {k: v for k, v in d.items() if v == v}
