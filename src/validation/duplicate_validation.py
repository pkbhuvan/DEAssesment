def remove_duplicate_members(df):
    """
    Remove duplicate member IDs and keep the record
    with the latest membership end date.
    """

    # Sort by latest membership end date
    df = df.sort_values(
        by="membership_end_date",
        ascending=False
    )

    # Remove duplicates
    df = df.drop_duplicates(
        subset="member_id",
        keep="first"
    )

    # Reset index
    df = df.reset_index(drop=True)

    return df