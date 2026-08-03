import pandas as pd


def validate_phone_numbers(df):
    """
    Validate phone numbers.
    A valid phone number should have exactly 10 digits.
    """

    def clean_phone(phone):

        if pd.isna(phone):
            return None

        phone = str(phone).strip()

        # Remove spaces, hyphens and brackets
        phone = (
            phone.replace("-", "")
                 .replace(" ", "")
                 .replace("(", "")
                 .replace(")", "")
        )

        if len(phone) == 10 and phone.isdigit():
            return phone

        return None

    df["phone_number"] = df["phone_number"].apply(clean_phone)

    return df