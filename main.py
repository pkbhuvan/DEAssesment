#from sqlalchemy import create_engine
from src.utils.logger import logger
#from src.database.load_data import load_dataframe
#from src.database.create_tables import create_tables
from src.parser.client_a_parser import ClientAParser
from src.utils.file_reader import (read_membership_files, read_claim_files)
from src.validation.date_validation import convert_dates
from src.validation.duplicate_validation import remove_duplicate_members
from src.validation.phone_validation import validate_phone_numbers
from src.validation.claim_validation import remove_invalid_claims
from src.validation.membership_date_validation import validate_membership_dates
from src.transformation.join_data import join_membership_claims


def main():

    # Create parser object (only for column standardization)
    parser = ClientAParser(None)
# ====================================================
# Membership Data
# ====================================================

    membership_df = read_membership_files()

    # Standardize column names FIRST
    membership_df = parser.standardize_columns(membership_df)

    # Convert dates
    membership_df = convert_dates(membership_df)

    # Validate membership dates
    membership_df = validate_membership_dates(membership_df)

    # Remove duplicate members
    membership_df = remove_duplicate_members(membership_df)

    # Validate phone numbers
    membership_df = validate_phone_numbers(membership_df)
    #create_tables()
    # load_dataframe(membership_df, "members")
    print("=" * 80)
    logger.info(f"Membership Records : {len(membership_df)}")

    # ====================================================
    # Claim Data
    # ====================================================

    claim_df = read_claim_files()

    claim_df = parser.standardize_claim_columns(claim_df)

    claim_df = remove_invalid_claims(claim_df)
    # load_dataframe(claim_df, "claims")
    print("=" * 80)
    logger.info(f"Claim Records : {len(claim_df)}")

    #====================================================
    # Join Membership + Claims
    # ====================================================

    # final_df = membership_df.merge(
    #     claim_df,
    #     on="member_id",
    #     how="inner"
    # )

    final_df = join_membership_claims(membership_df,claim_df)
    # load_dataframe(final_df, "member_claims")
    print(final_df.head())
    print("=" * 80)
    print("Final Joined Records :", len(final_df))
    print(final_df.head())
    

    # ====================================================
    # PostgreSQL
    # ====================================================

    # DATABASE_URL = "postgresql://postgres:password@localhost:5432/waymark"

    # engine = create_engine(DATABASE_URL)

    # final_df.to_sql(
    #     "member_claims",
    #     con=engine,
    #     if_exists="replace",
    #     index=False
    # )

    print("=" * 80)
    print("Data loaded successfully into PostgreSQL")


if __name__ == "__main__":
    main()