import pytest
import pandas as pd

from robopanda.robopanda import clean_column_names


def test_clean_column_names():
    df = pd.DataFrame({"Column/1": [1, 2, 3], "Column- 2": [4, 5, 6]})
    df = clean_column_names(df)
    assert df.columns.tolist() == ["column_1", "column_2"]


@pytest.mark.parametrize(
    "df",
    [
        pd.DataFrame({"Column 1": [1, 2, 3], "Column_1": [4, 5, 6]}),
        pd.DataFrame({"_data_": [1, 2, 3], "Column_2": [4, 5, 6]}),
    ],
)
def test_clean_column_names_with_name_collision(df):
    with pytest.raises(ValueError):
        df = clean_column_names(df)
