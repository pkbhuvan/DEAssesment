from src.utils.logger import logger

from src.parser.client_a_parser import ClientAParser

from src.utils.file_reader import (
    read_membership_files,
    read_claim_files,
    read_incremental_claim_files,
)

from src.validation.date_validation import convert_dates
from src.validation.duplicate_validation import remove_duplicate_members
from src.validation.phone_validation import validate_phone_numbers
from src.validation.claim_validation import remove_invalid_claims
from src.validation.membership_date_validation import validate_membership_dates

from src.transformation.join_data import join_membership_claims
from src.transformation.upsert_data import upsert_claims

from src.database.load_data import load_dataframe


def main():

    logger.info("Starting ETL Pipeline")

    parser = ClientAParser(None)

    # ====================================================
    # Membership Data Load
    # ====================================================

    membership_df = read_membership_files()

    print("=" * 80)
    print("Raw Membership Columns")
    print(membership_df.columns.tolist())

    membership_df = parser.standardize_columns(membership_df)

    membership_df = convert_dates(membership_df)

    membership_df = validate_membership_dates(membership_df)

    membership_df = remove_duplicate_members(membership_df)

    membership_df = validate_phone_numbers(membership_df)

    print("=" * 80)
    print("Membership Records:", len(membership_df))

    logger.info(f"Membership Records: {len(membership_df)}")

    # ====================================================
    # Claims Data Load
    # ====================================================

    claim_df = read_claim_files()

    print("=" * 80)
    print("Raw Claim Columns")
    print(claim_df.columns.tolist())

    claim_df = parser.standardize_claim_columns(claim_df)

    print("=" * 80)
    print("After Claim Standardization")
    print(claim_df.columns.tolist())
    print(claim_df.head())

    claim_df = remove_invalid_claims(claim_df)

    print("=" * 80)
    print("Claim Records:", len(claim_df))

    logger.info(f"Claim Records: {len(claim_df)}")

    # ====================================================
    # Validate Join Keys
    # ====================================================

    print("=" * 80)
    print("Membership IDs")
    print(membership_df["member_id"].head(10))

    print("Claim IDs")
    print(claim_df["member_id"].head(10))

    # ====================================================
    # Join Membership + Claims
    # ====================================================

    final_df = join_membership_claims(
        membership_df,
        claim_df
    )

    print("=" * 80)
    print("Final Joined Records:", len(final_df))
    print(final_df.head())

    logger.info(f"Final Joined Records: {len(final_df)}")

    # ====================================================
    # Load Initial Data
    # ====================================================

    try:

        load_dataframe(
            membership_df,
            "members"
        )

        load_dataframe(
            claim_df,
            "claims"
        )

        load_dataframe(
            final_df,
            "member_claims"
        )

        logger.info(
            "Initial data loaded successfully."
        )

    except Exception as e:

        logger.error(
            f"Initial database load failed: {e}"
        )

    # ====================================================
    # Incremental Claim Upsert (Set 2)
    # ====================================================

    print("=" * 80)
    print("Starting Incremental Claim Upsert")

    incremental_claims = read_incremental_claim_files()

    incremental_claims = parser.standardize_claim_columns(
        incremental_claims
    )

    incremental_claims = remove_invalid_claims(
        incremental_claims
    )

    updated_claims = upsert_claims(
        claim_df,
        incremental_claims
    )

    print("=" * 80)
    print("Existing Claims:", len(claim_df))
    print("After Upsert Claims:", len(updated_claims))
    print(updated_claims.head())

    logger.info(
        f"Claims After Upsert: {len(updated_claims)}"
    )

    # ====================================================
    # Recreate Final Joined Data
    # ====================================================

    updated_final_df = join_membership_claims(
        membership_df,
        updated_claims
    )

    # ====================================================
    # Missing Members (Requirement 7c)
    # ====================================================

    missing_members = membership_df[
        ~membership_df["member_id"].isin(
            updated_claims["member_id"]
        )
    ]

    print("=" * 80)
    print("Missing Members:", len(missing_members))

    logger.info(
        f"Missing Members: {len(missing_members)}"
    )

    # ====================================================
    # Load Updated Data
    # ====================================================

    try:

        load_dataframe(
            updated_claims,
            "claims"
        )

        load_dataframe(
            updated_final_df,
            "member_claims"
        )

        load_dataframe(
            missing_members,
            "missing_members"
        )

        logger.info(
            "Updated data loaded successfully."
        )

    except Exception as e:

        logger.error(
            f"Updated database load failed: {e}"
        )

    # ====================================================
    # Completion
    # ====================================================

    print("=" * 80)
    print("Data pipeline completed successfully")

    logger.info(
        "ETL Pipeline Completed Successfully"
    )


if __name__ == "__main__":
    main()