from src.utils.logger import logger

from src.utils.file_reader import (
    read_membership_files,
    read_claim_files,
    read_incremental_membership_files,
    read_incremental_claim_files,
)

from src.validation.date_validation import convert_dates
from src.validation.duplicate_validation import remove_duplicate_members
from src.validation.phone_validation import validate_phone_numbers
from src.validation.claim_validation import remove_invalid_claims
from src.validation.membership_date_validation import (
    validate_membership_dates
)

from src.transformation.join_data import (
    join_membership_claims
)

from src.transformation.upsert_data import (
    upsert_members,
    upsert_claims
)

from src.database.load_data import load_dataframe


def main():

    logger.info(
        "Starting ETL Pipeline"
    )

    # ====================================================
    # INITIAL MEMBERSHIP LOAD
    # Only TWO membership files
    # ====================================================

    print("=" * 80)
    print("INITIAL MEMBERSHIP LOAD")

    membership_df = read_membership_files()

    print(
        "Standardized Membership Columns:"
    )

    print(
        membership_df.columns.tolist()
    )

    # ----------------------------------------------------
    # Date conversion
    # ----------------------------------------------------

    membership_df = convert_dates(
        membership_df
    )

    # ----------------------------------------------------
    # Membership date validation
    # ----------------------------------------------------

    membership_df = validate_membership_dates(
        membership_df
    )

    # ----------------------------------------------------
    # Remove duplicate members
    # ----------------------------------------------------

    membership_df = remove_duplicate_members(
        membership_df
    )

    # ----------------------------------------------------
    # Phone validation
    # ----------------------------------------------------

    membership_df = validate_phone_numbers(
        membership_df
    )

    print(
        "Membership Records:",
        len(membership_df)
    )

    logger.info(
        f"Membership Records: {len(membership_df)}"
    )

    # ====================================================
    # INITIAL CLAIM LOAD
    # Only TWO claim files
    # ====================================================

    print("=" * 80)
    print("INITIAL CLAIM LOAD")

    claim_df = read_claim_files()

    print(
        "Standardized Claim Columns:"
    )

    print(
        claim_df.columns.tolist()
    )

    print(
        claim_df.head()
    )

    # ----------------------------------------------------
    # Remove invalid claims
    # ----------------------------------------------------

    claim_df = remove_invalid_claims(
        claim_df
    )

    print(
        "Claim Records:",
        len(claim_df)
    )

    logger.info(
        f"Claim Records: {len(claim_df)}"
    )

    # ====================================================
    # JOIN MEMBERSHIP + CLAIMS
    # ====================================================

    print("=" * 80)
    print("JOIN MEMBERSHIP + CLAIMS")

    print(
        "Membership IDs:"
    )

    print(
        membership_df["member_id"].head(10)
    )

    print(
        "Claim Member IDs:"
    )

    print(
        claim_df["member_id"].head(10)
    )

    final_df = join_membership_claims(
        membership_df,
        claim_df
    )

    print(
        "Final Joined Records:",
        len(final_df)
    )

    print(
        final_df.head()
    )

    logger.info(
        f"Initial Joined Records: {len(final_df)}"
    )

    # ====================================================
    # INITIAL DATABASE LOAD
    # ====================================================

    print("=" * 80)
    print("INITIAL DATABASE LOAD")

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
            "Initial database load completed successfully."
        )

    except Exception as e:

        logger.error(
            f"Initial database load failed: {e}"
        )

        raise

    # ====================================================
    # SET 2
    # INCREMENTAL MEMBERSHIP
    # Third membership file only
    # ====================================================

    print("=" * 80)
    print("INCREMENTAL MEMBERSHIP UPSERT")

    incremental_members = (
        read_incremental_membership_files()
    )

    print(
        "Incremental Membership Columns:"
    )

    print(
        incremental_members.columns.tolist()
    )

    # ----------------------------------------------------
    # Apply same validations to incremental membership
    # ----------------------------------------------------

    incremental_members = convert_dates(
        incremental_members
    )

    incremental_members = validate_membership_dates(
        incremental_members
    )

    incremental_members = validate_phone_numbers(
        incremental_members
    )

    # ----------------------------------------------------
    # Membership Upsert
    # ----------------------------------------------------

    updated_members = upsert_members(
        membership_df,
        incremental_members
    )

    print(
        "Existing Members:",
        len(membership_df)
    )

    print(
        "Incremental Members:",
        len(incremental_members)
    )

    print(
        "Members After Upsert:",
        len(updated_members)
    )

    logger.info(
        f"Members After Upsert: {len(updated_members)}"
    )

    # ====================================================
    # SET 2
    # INCREMENTAL CLAIM
    # Third claim file only
    # ====================================================

    print("=" * 80)
    print("INCREMENTAL CLAIM UPSERT")

    incremental_claims = (
        read_incremental_claim_files()
    )

    print(
        "Incremental Claim Columns:"
    )

    print(
        incremental_claims.columns.tolist()
    )

    incremental_claims = (
        remove_invalid_claims(
            incremental_claims
        )
    )

    # ----------------------------------------------------
    # Claim Upsert
    # ----------------------------------------------------

    updated_claims = upsert_claims(
        claim_df,
        incremental_claims
    )

    print(
        "Existing Claims:",
        len(claim_df)
    )

    print(
        "Incremental Claims:",
        len(incremental_claims)
    )

    print(
        "Claims After Upsert:",
        len(updated_claims)
    )

    logger.info(
        f"Claims After Upsert: {len(updated_claims)}"
    )

    # ====================================================
    # REBUILD FINAL RELATIONSHIP
    # ====================================================

    print("=" * 80)
    print("REBUILDING MEMBER + CLAIM RELATIONSHIP")

    updated_final_df = join_membership_claims(
        updated_members,
        updated_claims
    )

    print(
        "Updated Final Joined Records:",
        len(updated_final_df)
    )

    # ====================================================
    # FIND MISSING MEMBERS
    # ====================================================

    missing_members = updated_members[
        ~updated_members["member_id"].isin(
            updated_claims["member_id"]
        )
    ].copy()

    print(
        "Missing Members:",
        len(missing_members)
    )

    logger.info(
        f"Missing Members: {len(missing_members)}"
    )

    # ====================================================
    # LOAD UPDATED DATA
    # ====================================================

    print("=" * 80)
    print("LOADING UPDATED DATA")

    try:

        load_dataframe(
            updated_members,
            "members"
        )

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
            "Updated database load completed successfully."
        )

    except Exception as e:

        logger.error(
            f"Updated database load failed: {e}"
        )

        raise

    # ====================================================
    # COMPLETION
    # ====================================================

    print("=" * 80)
    print(
        "Data pipeline completed successfully"
    )

    logger.info(
        "ETL Pipeline Completed Successfully"
    )


if __name__ == "__main__":
    main()