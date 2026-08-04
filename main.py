from src.parser.client_a_parser import ClientAParser
from src.validation.claim_validation import remove_invalid_claims


def main():

    # ---------------- Membership ----------------
    membership_parser = ClientAParser(
        "data/raw/Patient-membership-clientA-202307.xlsx"
    )

    membership_df = membership_parser.read_file()

    membership_df = membership_parser.standardize_columns(membership_df)

    print("Membership Data")
    print(membership_df.head())

    print("=" * 80)

    # ---------------- Claims ----------------
    claim_parser = ClientAParser(
        "data/raw/Patient-claim-clientA-202307.xlsx"
    )

    claim_df = claim_parser.read_file()
    claim_df = claim_parser.read_file()

    claim_df = claim_parser.standardize_claim_columns(claim_df)
    claim_df = remove_invalid_claims(claim_df)

    print(claim_df.columns.tolist())

    print("Claim Data")
    print(claim_df.head())
    final_df = membership_df.merge(claim_df,on="member_id",how="inner")

    print("Final Joined Records:", len(final_df))

    print(final_df.head())


if __name__ == "__main__":
    main()