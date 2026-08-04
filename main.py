from src.utils.logger import logger

from src.parser.client_a_parser import ClientAParser

from src.utils.file_reader import (
    read_membership_files,
    read_claim_files,
    read_incremental_claim_files
)

from src.validation.date_validation import convert_dates
from src.validation.duplicate_validation import remove_duplicate_members
from src.validation.phone_validation import validate_phone_numbers
from src.validation.claim_validation import remove_invalid_claims
from src.validation.membership_date_validation import validate_membership_dates

from src.transformation.join_data import join_membership_claims

from src.transformation.upsert_data import upsert_claims



def main():

    parser = ClientAParser(None)


    # ====================================================
    # Membership Data Load
    # ====================================================

    membership_df = read_membership_files()

    print("=" * 80)
    print("Raw Membership Columns")
    print(membership_df.columns.tolist())


    # Standardize membership columns

    membership_df = (
        parser.standardize_columns(
            membership_df
        )
    )


    # Convert dates

    membership_df = convert_dates(
        membership_df
    )


    # Validate membership dates

    membership_df = validate_membership_dates(
        membership_df
    )


    # Remove duplicate members

    membership_df = remove_duplicate_members(
        membership_df
    )


    # Validate phone numbers

    membership_df = validate_phone_numbers(
        membership_df
    )


    print("=" * 80)

    print(
        "Membership Records:",
        len(membership_df)
    )



    # ====================================================
    # Claims Data Load
    # ====================================================


    claim_df = read_claim_files()


    print("=" * 80)

    print("Raw Claim Columns")

    print(
        claim_df.columns.tolist()
    )



    # Standardize claim columns

    claim_df = (
        parser.standardize_claim_columns(
            claim_df
        )
    )


    print("=" * 80)

    print("After Claim Standardization")

    print(
        claim_df.columns.tolist()
    )


    print(
        claim_df.head()
    )



    # Remove claims without claim number

    claim_df = remove_invalid_claims(
        claim_df
    )


    print("=" * 80)

    print(
        "Claim Records:",
        len(claim_df)
    )



    # ====================================================
    # Validate Join Keys
    # ====================================================


    print("=" * 80)

    print("Membership IDs")

    print(
        membership_df["member_id"]
        .head(10)
    )


    print("Claim IDs")

    print(
        claim_df["member_id"]
        .head(10)
    )



    # ====================================================
    # Join Membership + Claims
    # ====================================================


    final_df = join_membership_claims(
        membership_df,
        claim_df
    )



    print("=" * 80)

    print(
        "Final Joined Records:",
        len(final_df)
    )


    print(
        final_df.head()
    )



    # ====================================================
    # Incremental Claim Upsert Test
    # Set 2
    # ====================================================


    print("=" * 80)

    print(
        "Starting Incremental Claim Upsert"
    )


    incremental_claims = (
        read_incremental_claim_files()
    )


    incremental_claims = (
        parser.standardize_claim_columns(
            incremental_claims
        )
    )



    incremental_claims = (
        remove_invalid_claims(
            incremental_claims
        )
    )



    updated_claims = upsert_claims(
        claim_df,
        incremental_claims
    )


    print("=" * 80)

    print(
        "Existing Claims:",
        len(claim_df)
    )


    print(
        "After Upsert Claims:",
        len(updated_claims)
    )


    print(
        updated_claims.head()
    )



    # ====================================================
    # Completion
    # ====================================================


    print("=" * 80)

    print(
        "Data pipeline completed successfully"
    )



if __name__ == "__main__":

    main()