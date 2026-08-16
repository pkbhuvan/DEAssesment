import pandas as pd


# ============================================================
# Membership Upsert
# ============================================================

def upsert_members(
    existing_members,
    incremental_members
):
    """
    Upsert membership records using member_id as the business key.

    Existing member:
        Update the existing record.

    New member:
        Insert the new record.
    """

    existing = existing_members.copy()
    incremental = incremental_members.copy()

    # --------------------------------------------------------
    # Ensure member_id exists
    # --------------------------------------------------------

    if "member_id" not in existing.columns:
        raise ValueError(
            "Existing membership data must contain member_id"
        )

    if "member_id" not in incremental.columns:
        raise ValueError(
            "Incremental membership data must contain member_id"
        )

    # --------------------------------------------------------
    # Standardize IDs
    # --------------------------------------------------------

    existing["member_id"] = (
        existing["member_id"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.strip()
    )

    incremental["member_id"] = (
        incremental["member_id"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.strip()
    )

    # --------------------------------------------------------
    # Incremental data takes priority
    # --------------------------------------------------------

    combined = pd.concat(
        [
            existing,
            incremental
        ],
        ignore_index=True
    )

    # --------------------------------------------------------
    # Keep latest record for each member
    # Incremental records appear last, therefore they win.
    # --------------------------------------------------------

    combined = combined.drop_duplicates(
        subset=["member_id"],
        keep="last"
    )

    combined = combined.reset_index(
        drop=True
    )

    print(
        "Existing members:",
        len(existing)
    )

    print(
        "Incremental members:",
        len(incremental)
    )

    print(
        "Members after upsert:",
        len(combined)
    )

    return combined


# ============================================================
# Claim Upsert
# ============================================================

def upsert_claims(
    existing_claims,
    incremental_claims
):
    """
    Upsert claims using claim_number as the business key.

    Existing claim:
        Update the existing record.

    New claim:
        Insert the new record.
    """

    existing = existing_claims.copy()
    incremental = incremental_claims.copy()

    if "claim_number" not in existing.columns:
        raise ValueError(
            "Existing claims must contain claim_number"
        )

    if "claim_number" not in incremental.columns:
        raise ValueError(
            "Incremental claims must contain claim_number"
        )

    # --------------------------------------------------------
    # Remove null claim numbers
    # --------------------------------------------------------

    existing = existing[
        existing["claim_number"].notna()
    ].copy()

    incremental = incremental[
        incremental["claim_number"].notna()
    ].copy()

    # --------------------------------------------------------
    # Standardize claim IDs
    # --------------------------------------------------------

    existing["claim_number"] = (
        existing["claim_number"]
        .astype(str)
        .str.strip()
    )

    incremental["claim_number"] = (
        incremental["claim_number"]
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # Incremental data takes priority
    # --------------------------------------------------------

    combined = pd.concat(
        [
            existing,
            incremental
        ],
        ignore_index=True
    )

    combined = combined.drop_duplicates(
        subset=["claim_number"],
        keep="last"
    )

    combined = combined.reset_index(
        drop=True
    )

    print(
        "Existing claims:",
        len(existing)
    )

    print(
        "Incremental claims:",
        len(incremental)
    )

    print(
        "Claims after upsert:",
        len(combined)
    )

    return combined