import pandas as pd
from src.validation.claim_validation import remove_invalid_claims
def test_remove_invalid_claims():

    df = pd.DataFrame({
        "claim_number": [
            "ABC123",
            None,
            "XYZ456"
        ]
    })

    result = remove_invalid_claims(df)

    assert len(result) == 2
    assert result["claim_number"].isna().sum() == 0
