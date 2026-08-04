import pandas as pd
from src.validation.phone_validation import validate_phone_numbers
def test_validate_phone_numbers():

    df = pd.DataFrame({
        "phone_number": [
            "9876543210",
            "12345",
            None
        ]
    })

    result = validate_phone_numbers(df)

    assert result.loc[0, "phone_number"] == "9876543210"
    assert result.loc[1, "phone_number"] is None
    assert result.loc[2, "phone_number"] is None