import pandas as pd

from src.validation.duplicate_validation import remove_duplicate_members


def test_remove_duplicate_members():

    df = pd.DataFrame({
        "member_id": [1, 1, 2],
        "membership_end_date": [
            "2023-12-31",
            "2023-11-30",
            "2023-12-31"
        ]
    })

    df["membership_end_date"] = pd.to_datetime(df["membership_end_date"])

    result = remove_duplicate_members(df)

    assert len(result) == 2
    assert result["member_id"].duplicated().sum() == 0