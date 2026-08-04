import pandas as pd

from src.parser.client_a_parser import ClientAParser


def test_standardize_membership_columns():

    parser = ClientAParser("dummy.xlsx")

    df = pd.DataFrame(columns=[
        "member id",
        "member first name",
        "phone number"
    ])

    result = parser.standardize_columns(df)

    assert "member_id" in result.columns
    assert "first_name" in result.columns
    assert "phone_number" in result.columns


def test_standardize_claim_columns():

    parser = ClientAParser("dummy.xlsx")

    df = pd.DataFrame(columns=[
        "claim category",
        "member id",
        "claim number"
    ])

    result = parser.standardize_claim_columns(df)

    assert "claim_category" in result.columns
    assert "member_id" in result.columns
    assert "claim_number" in result.columns