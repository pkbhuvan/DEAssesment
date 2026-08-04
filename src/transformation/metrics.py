def calculate_total_billed(df):

    result = (
        df.groupby("member_id")["total_billed"]
        .sum()
        .reset_index()
    )

    result.rename(
        columns={"total_billed": "total_claim_amount"},
        inplace=True
    )

    return result