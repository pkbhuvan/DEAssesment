def remove_invalid_claims(df):
    """
    Remove claims where claim id is missing.
    Supports Client A and Client B formats.
    """

    before = len(df)

    # Create common claim_number column
    if "claim number" in df.columns:
        df["claim_number"] = df["claim_number"].fillna(
            df["claim number"]
        )

    # Remove records without claim number
    df = df.dropna(subset=["claim_number"])

    after = len(df)

    print(f"Claims before validation : {before}")
    print(f"Claims after validation  : {after}")

    return df.reset_index(drop=True)