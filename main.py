from src.parser.client_a_parser import ClientAParser
from src.validation.date_validation import convert_dates
from src.validation.duplicate_validation import remove_duplicate_members
from src.validation.phone_validation import validate_phone_numbers


def main():

    parser = ClientAParser(
        "data/raw/Patient-membership-clientA-202307.xlsx"
    )

    df = parser.read_file()

    df = parser.standardize_columns(df)

    df = convert_dates(df)

    print("Before removing duplicates:", len(df))

    # Check duplicates BEFORE removing them
    print("Duplicate member IDs:",
          df["member_id"].duplicated().sum())

    df = remove_duplicate_members(df)

    print("After removing duplicates:", len(df))
    df = validate_phone_numbers(df)

    print(df[["member_id", "phone_number"]].head())
    

    print(df.head())


if __name__ == "__main__":
    main()