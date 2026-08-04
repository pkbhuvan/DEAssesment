def remove_invalid_claims(df):
    """
    Remove claims where claim_number is missing.
    """

    before = len(df)

    df = df.dropna(subset=["claim_number"])

    after = len(df)

    print(f"Claims before validation : {before}")
    print(f"Claims after validation  : {after}")

    return df.reset_index(drop=True)
