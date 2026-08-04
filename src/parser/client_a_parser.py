import pandas as pd


class ClientAParser:

    def __init__(self, file_path):
        self.file_path = file_path


    def read_file(self):
        return pd.read_excel(self.file_path)


    def standardize_columns(self, df):
        """
        Standardize membership columns for Client A and Client B
        """

        column_mapping = {
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
            "ethnicity": "ethnicity"
        }

        df.rename(
            columns=column_mapping,
            inplace=True
        )

        # Handle Client B member id
        if "mem_id" in df.columns:

            df["member_id"] = df["member_id"].fillna(
                df["mem_id"]
            )

        return df



    def standardize_claim_columns(self, df):
        """
        Standardize claim columns for Client A and Client B
        """

        df = df.copy()


        # ==============================
        # Client A column mapping
        # ==============================

        rename_map = {
            "claim number": "claim_number",
            "member id": "member_id",
            "date received": "date_received",
            "hospital service": "hospital_service",
            "coding system": "code_system",
            "total billed": "cost_total",
            "processing status": "status"
        }


        df.rename(
            columns=rename_map,
            inplace=True
        )


        # ==============================
        # Combine duplicate claim_number
        # ==============================

        claim_cols = df.loc[:, df.columns == "claim_number"]

        if claim_cols.shape[1] > 1:

            df["claim_number"] = (
                claim_cols
                .bfill(axis=1)
                .iloc[:, 0]
            )


        # ==============================
        # Combine member_id
        # ==============================

        if "memb_id" in df.columns:

            df["member_id"] = (
                df["member_id"]
                .fillna(df["memb_id"])
            )

            df.drop(
                columns=["memb_id"],
                inplace=True
            )


        # ==============================
        # Combine received date
        # ==============================

        if "received_date" in df.columns:

            df["date_received"] = (
                df["date_received"]
                .fillna(df["received_date"])
            )

            df.drop(
                columns=["received_date"],
                inplace=True
            )


        # ==============================
        # Remove duplicate columns
        # ==============================

        df = df.loc[
            :,
            ~df.columns.duplicated()
        ]


        return df