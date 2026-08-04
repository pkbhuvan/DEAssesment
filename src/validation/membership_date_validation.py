import pandas as pd


def validate_membership_dates(df):
    """
    Validate membership dates.
    Rules:
    1. Membership end date should not be before date of birth.
    2. Remove records with invalid dates.
    """

    before = len(df)

    df["date_of_birth"] = pd.to_datetime(df["date_of_birth"], errors="coerce")
    df["membership_end_date"] = pd.to_datetime(
        df["membership_end_date"], errors="coerce"
    )

    df = df.dropna(subset=["date_of_birth", "membership_end_date"])

    df = df[df["membership_end_date"] >= df["date_of_birth"]]

    after = len(df)

    print(f"Membership records before date validation : {before}")
    print(f"Membership records after date validation  : {after}")

    return df.reset_index(drop=True)