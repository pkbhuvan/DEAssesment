from sqlalchemy import create_engine

from src.parser.client_a_parser import ClientAParser
from src.validation.date_validation import convert_dates
from src.validation.duplicate_validation import remove_duplicate_members
from src.validation.phone_validation import validate_phone_numbers
from src.validation.claim_validation import remove_invalid_claims


def main():

    # ---------------- Membership ----------------

    membership_parser = ClientAParser(
        "data/raw/Patient-membership-clientA-202307.xlsx"
    )

    membership_df = membership_parser.read_file()

    membership_df = membership_parser.standardize_columns(membership_df)

    membership_df = convert_dates(membership_df)

    membership_df = remove_duplicate_members(membership_df)

    membership_df = validate_phone_numbers(membership_df)

    print("Membership Records :", len(membership_df))

    print("=" * 80)

    # ---------------- Claims ----------------

    claim_parser = ClientAParser(
        "data/raw/Patient-claim-clientA-202307.xlsx"
    )

    claim_df = claim_parser.read_file()

    claim_df = claim_parser.standardize_claim_columns(claim_df)

    claim_df = remove_invalid_claims(claim_df)

    print("Claim Records :", len(claim_df))

    print("=" * 80)

    # ---------------- Join ----------------

    final_df = membership_df.merge(
        claim_df,
        on="member_id",
        how="inner"
    )

    print("Final Joined Records :", len(final_df))

    print(final_df.head())

    # ---------------- PostgreSQL ----------------

    DATABASE_URL = "postgresql://postgres:password@localhost:5432/waymark"

    engine = create_engine(DATABASE_URL)

    final_df.to_sql(
        "member_claims",
        engine,
        if_exists="replace",
        index=False
    )

    print("Data loaded successfully into PostgreSQL")


if __name__ == "__main__":
    main()