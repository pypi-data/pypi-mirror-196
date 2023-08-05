import re

import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Clean column names to snake case. This enables the use of dot notation to access columns.

    Parameters
    ----------
    df : pd.DataFrame
        A pandas DataFrame with columns to be cleaned.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame with cleaned column names.

    Raises
    ------
    ValueError
        If there are any name collisions with other columns or existing pd.DataFrame attributes or methods.
    """
    replacements = [
        (
            r"[\s/-]",
            "_",
        ),  # replace spaces, dashes, and forward slashes with underscores
        (r"[_]{2,}", "_"),  # replace multiple underscores with a single underscore
        (
            r"[^a-zA-Z\d\s_]",
            "",
        ),  # remove all non-alphanumeric characters except underscores
    ]

    updated_column_names = df.columns.to_list()

    for str_replacement in replacements:
        updated_column_names = [re.sub(*str_replacement, col) for col in updated_column_names]

    updated_column_names = [col.lower() for col in updated_column_names]

    column_name_collision = len(set(updated_column_names)) < len(updated_column_names)
    dataframe_attribute_collision = len(set(updated_column_names) & set(dir(df))) > 0

    if column_name_collision:
        raise ValueError("There are duplicate column names.")
    if dataframe_attribute_collision:
        raise ValueError("There are column names that conflict with pd.DataFrame attributes or methods.")

    replacement_dict = {old_name: new_name for old_name, new_name in zip(df.columns.tolist(), updated_column_names)}
    return df.rename(columns=replacement_dict)
