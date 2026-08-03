import pandas as pd


def convert_dates(df):
    """
    Convert date columns to datetime format.
    Invalid dates will become NaT.
    """

    date_columns = [
        "date_of_birth",
        "membership_end_date"
    ]

    for column in date_columns:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

    return df