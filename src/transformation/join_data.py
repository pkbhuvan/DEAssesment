import pandas as pd


def join_membership_claims(membership_df, claim_df):
    """
    Join membership and claim data on member_id.
    """

    final_df = membership_df.merge(
        claim_df,
        on="member_id",
        how="inner"
    )

    print("=" * 80)
    print(f"Final Joined Records : {len(final_df)}")

    return final_df