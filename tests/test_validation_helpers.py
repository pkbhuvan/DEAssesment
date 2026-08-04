import pandas as pd

from src.validation.gender_validation import validate_gender
from src.validation.membership_date_validation import validate_membership_dates
from src.validation.zip_validation import validate_zip
from src.validation.missing_value_validation import handle_missing_values


def test_validate_gender_keeps_only_valid_values():
    df = pd.DataFrame({"gender": ["M", "F", "X", "m"]})

    result = validate_gender(df)

    assert list(result["gender"]) == ["M", "F"]


def test_validate_membership_dates_removes_invalid_rows():
    df = pd.DataFrame(
        {
            "date_of_birth": ["1990-01-01", "2000-01-01", "bad-date"],
            "membership_end_date": ["1995-01-01", "1999-12-31", "2020-01-01"],
        }
    )

    result = validate_membership_dates(df)

    assert len(result) == 1
    assert result.iloc[0]["date_of_birth"] == pd.Timestamp("1990-01-01")
    assert result.iloc[0]["membership_end_date"] == pd.Timestamp("1995-01-01")


def test_validate_zip_keeps_five_digit_codes_only():
    df = pd.DataFrame({"zip_code": [12345, "1234", "ABCDE", 67890]})

    result = validate_zip(df)

    assert list(result["zip_code"]) == ["12345", "ABCDE", "67890"]


def test_handle_missing_values_fills_unknowns():
    df = pd.DataFrame({"ethnicity": [None, "Asian"], "state": [None, "CA"]})

    result = handle_missing_values(df)

    assert result.loc[0, "ethnicity"] == "Unknown"
    assert result.loc[0, "state"] == "Unknown"
    assert result.loc[1, "ethnicity"] == "Asian"
    assert result.loc[1, "state"] == "CA"
