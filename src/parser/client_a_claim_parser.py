import pandas as pd


class ClientAClaimParser:

    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        return pd.read_excel(self.file_path)

    def standardize_columns(self, df):

        column_mapping = {
            "claim category": "claim_category",
            "member id": "member_id",
            "claim number": "claim_number",
            "date received": "date_received",
            "vendor": "vendor",
            "hospital service": "hospital_service",
            "coding system": "coding_system",
            "code": "code",
            "primary diagnosis": "primary_diagnosis",
            "total billed": "total_billed",
            "processing status": "processing_status"
        }

        df.rename(columns=column_mapping, inplace=True)

        return df
