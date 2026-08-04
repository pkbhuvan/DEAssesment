import pandas as pd


class ClientAParser:

    def __init__(self, file_path):
        self.file_path = file_path


    def read_file(self):

        return pd.read_excel(
            self.file_path
        )



    # ====================================================
    # Membership Column Standardization
    # ====================================================

    def standardize_columns(self, df):

        """
        Standardize membership columns
        Client A + Client B
        """

        df = df.copy()


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



        # Client B member id

        if "mem_id" in df.columns:

            if "member_id" in df.columns:

                df["member_id"] = (
                    df["member_id"]
                    .fillna(df["mem_id"])
                )

            else:

                df["member_id"] = df["mem_id"]



        # Standardize member id datatype

        if "member_id" in df.columns:

            df["member_id"] = (

                df["member_id"]
                .astype(str)
                .str.replace(
                    ".0",
                    "",
                    regex=False
                )
                .str.strip()

            )


        return df




    # ====================================================
    # Claim Column Standardization
    # ====================================================

    def standardize_claim_columns(self, df):

        """
        Standardize claim columns
        Client A + Client B
        """

        df = df.copy()



        rename_map = {


            "claim category": "claim_category",

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



        # =================================================
        # Handle duplicate claim_number columns
        # =================================================


        claim_cols = df.loc[
            :,
            df.columns == "claim_number"
        ]


        if claim_cols.shape[1] > 1:

            df["claim_number"] = (

                claim_cols
                .bfill(axis=1)
                .iloc[:,0]

            )



        # =================================================
        # Client B member id
        # =================================================


        if "memb_id" in df.columns:


            if "member_id" in df.columns:

                df["member_id"] = (

                    df["member_id"]
                    .fillna(df["memb_id"])

                )

            else:

                df["member_id"] = df["memb_id"]



            df.drop(
                columns=["memb_id"],
                inplace=True
            )



        # =================================================
        # Client B received date
        # =================================================


        if "received_date" in df.columns:


            if "date_received" in df.columns:

                df["date_received"] = (

                    df["date_received"]
                    .fillna(df["received_date"])

                )

            else:

                df["date_received"] = df["received_date"]



            df.drop(
                columns=["received_date"],
                inplace=True
            )



        # =================================================
        # Member ID datatype
        # =================================================


        if "member_id" in df.columns:


            df["member_id"] = (

                df["member_id"]
                .astype(str)
                .str.replace(
                    ".0",
                    "",
                    regex=False
                )
                .str.strip()

            )



        # =================================================
        # Remove duplicate columns
        # =================================================


        df = df.loc[:, ~df.columns.duplicated()]



        return df