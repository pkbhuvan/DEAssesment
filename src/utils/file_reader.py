import os
import pandas as pd


RAW_DATA_PATH = "data/raw"


# ============================================================
# Set 1 - Initial Load
# Only TWO membership files
# Only TWO claim files
# ============================================================

SET1_MEMBERSHIP_FILES = [
    "Patient-membership-clientA-202307.xlsx",
    "Patient-membership-clientB-202307.xlsx",
]

SET1_CLAIM_FILES = [
    "Patient-claim-clientA-202307.xlsx",
    "Patient-claim-clientB-202307.xlsx",
]


# ============================================================
# Set 2 - Incremental Load
# Third file is processed only during upsert
# ============================================================

SET2_MEMBERSHIP_FILES = [
    "Patient-membership-clientA-202308.xlsx",
]

SET2_CLAIM_FILES = [
    "Patient-claim-clientA-202308.xlsx",
]


# ============================================================
# Helper
# ============================================================

def _read_files(file_names, description):
    """
    Read multiple Excel files and combine them into one DataFrame.
    """

    dataframes = []

    for file_name in file_names:

        file_path = os.path.join(
            RAW_DATA_PATH,
            file_name
        )

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"{description} file not found: {file_path}"
            )

        print(f"Reading {file_path}")

        df = pd.read_excel(file_path)

        dataframes.append(df)

    if not dataframes:
        raise ValueError(
            f"No {description} files were found."
        )

    return pd.concat(
        dataframes,
        ignore_index=True
    )


# ============================================================
# Membership Standardization
# ============================================================

def standardize_membership_columns(df):
    """
    Standardize Client A and Client B membership columns.

    Equivalent Client A / Client B columns are converted into
    one canonical column.
    """

    df = df.copy()

    # --------------------------------------------------------
    # Normalize column names
    # --------------------------------------------------------

    df.columns = [
        str(col).strip()
        for col in df.columns
    ]

    # --------------------------------------------------------
    # Direct Client A -> canonical mapping
    # --------------------------------------------------------

    rename_map = {
        "member id": "member_id",
        "member first name": "first_name",
        "member middle name": "middle_name",
        "member last name": "last_name",
        "gender": "gender",
        "date of birth": "date_of_birth",
        "address": "address",
        "city": "city",
        "state": "state",
        "zip": "zip_code",
        "phone number": "phone_number",
        "membership end date": "membership_end_date",
        "ethnicity": "ethnicity",
    }

    df.rename(
        columns=rename_map,
        inplace=True
    )

    # --------------------------------------------------------
    # Client B columns
    # Coalesce Client B fields into canonical fields
    # --------------------------------------------------------

    column_groups = {
        "member_id": ["member_id", "mem_id"],
        "first_name": ["first_name", "Member_Fullname"],
        "date_of_birth": ["date_of_birth", "Dob"],
        "gender": ["gender", "Gender"],
        "address": ["address", "Member_Address"],
        "city": ["city", "Member_City"],
        "state": ["state", "Member_State"],
        "zip_code": ["zip_code", "Member_Zip"],
        "phone_number": ["phone_number", "Member_Phone"],
    }

    for target_column, source_columns in column_groups.items():

        existing_columns = [
            column
            for column in source_columns
            if column in df.columns
        ]

        if not existing_columns:
            continue

        # Start with first available column
        combined = df[existing_columns[0]]

        # Fill missing values from other equivalent columns
        for column in existing_columns[1:]:
            combined = combined.fillna(
                df[column]
            )

        df[target_column] = combined

    # --------------------------------------------------------
    # Remove source Client B columns
    # --------------------------------------------------------

    client_b_columns = [
        "mem_id",
        "Member_Fullname",
        "Dob",
        "Age_In_Mths_No",
        "Gender",
        "Member_Address",
        "Member_Address_2",
        "Member_City",
        "Member_State",
        "Member_Zip",
        "Member_Phone",
    ]

    columns_to_drop = [
        column
        for column in client_b_columns
        if column in df.columns
        and column not in [
            "member_id",
            "first_name",
            "date_of_birth",
            "gender",
            "address",
            "city",
            "state",
            "zip_code",
            "phone_number",
        ]
    ]

    df.drop(
        columns=columns_to_drop,
        inplace=True,
        errors="ignore"
    )

    # --------------------------------------------------------
    # Standardize member_id
    # --------------------------------------------------------

    if "member_id" in df.columns:

        df["member_id"] = (
            df["member_id"]
            .astype(str)
            .str.replace(".0", "", regex=False)
            .str.strip()
        )

        df["member_id"] = df["member_id"].replace(
            {
                "nan": None,
                "None": None,
                "": None
            }
        )

    # --------------------------------------------------------
    # Remove duplicate columns
    # --------------------------------------------------------

    df = df.loc[
        :,
        ~df.columns.duplicated()
    ]

    return df


# ============================================================
# Claim Standardization
# ============================================================

def standardize_claim_columns(df):
    """
    Standardize Client A and Client B claim columns.
    """

    df = df.copy()

    df.columns = [
        str(col).strip()
        for col in df.columns
    ]

    # --------------------------------------------------------
    # Client A mappings
    # --------------------------------------------------------

    rename_map = {
        "claim category": "claim_category",
        "member id": "member_id",
        "claim number": "claim_number",
        "date received": "date_received",
        "vendor": "vendor",
        "hospital service": "hospital_service",
        "coding system": "code_system",
        "code": "code",
        "primary diagnosis": "primary_diagnosis",
        "total billed": "cost_total",
        "processing status": "status",
    }

    df.rename(
        columns=rename_map,
        inplace=True
    )

    # --------------------------------------------------------
    # Client B mappings
    # --------------------------------------------------------

    column_groups = {
        "claim_category": [
            "claim_category",
            "claim category"
        ],

        "member_id": [
            "member_id",
            "memb_id"
        ],

        "claim_number": [
            "claim_number",
            "claim number"
        ],

        "date_received": [
            "date_received",
            "received_date"
        ],

        "hospital_service": [
            "hospital_service"
        ],

        "code_system": [
            "code_system"
        ],

        "cost_total": [
            "cost_total"
        ],

        "status": [
            "status"
        ],

        "diagnosis_type": [
            "diagnosis_type"
        ],
    }

    # --------------------------------------------------------
    # Coalesce equivalent columns
    # --------------------------------------------------------

    for target_column, source_columns in column_groups.items():

        existing_columns = [
            column
            for column in source_columns
            if column in df.columns
        ]

        if not existing_columns:
            continue

        combined = df[existing_columns[0]]

        for column in existing_columns[1:]:

            combined = combined.fillna(
                df[column]
            )

        df[target_column] = combined

    # --------------------------------------------------------
    # Standardize member ID
    # --------------------------------------------------------

    if "member_id" in df.columns:

        df["member_id"] = (
            df["member_id"]
            .astype(str)
            .str.replace(".0", "", regex=False)
            .str.strip()
        )

        df["member_id"] = df["member_id"].replace(
            {
                "nan": None,
                "None": None,
                "": None
            }
        )

    # --------------------------------------------------------
    # Remove duplicate columns
    # --------------------------------------------------------

    df = df.loc[
        :,
        ~df.columns.duplicated()
    ]

    return df


# ============================================================
# Initial Membership Load
# ============================================================

def read_membership_files():

    df = _read_files(
        SET1_MEMBERSHIP_FILES,
        "Membership"
    )

    return standardize_membership_columns(df)


# ============================================================
# Initial Claim Load
# ============================================================

def read_claim_files():

    df = _read_files(
        SET1_CLAIM_FILES,
        "Claim"
    )

    return standardize_claim_columns(df)


# ============================================================
# Incremental Membership Load
# ============================================================

def read_incremental_membership_files():

    df = _read_files(
        SET2_MEMBERSHIP_FILES,
        "Incremental membership"
    )

    return standardize_membership_columns(df)


# ============================================================
# Incremental Claim Load
# ============================================================

def read_incremental_claim_files():

    df = _read_files(
        SET2_CLAIM_FILES,
        "Incremental claim"
    )

    return standardize_claim_columns(df)