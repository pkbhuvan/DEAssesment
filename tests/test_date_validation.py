import pandas as pd

from src.validation.date_validation import convert_dates


def test_convert_dates():

    df = pd.DataFrame({
        "date_of_birth": ["1995-01-10"],
        "membership_end_date": ["2023-12-31"]
    })

    result = convert_dates(df)

    assert pd.api.types.is_datetime64_any_dtype(result["date_of_birth"])
    assert pd.api.types.is_datetime64_any_dtype(result["membership_end_date"])