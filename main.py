from src.parser.client_a_parser import ClientAParser
from src.validation.date_validation import convert_dates


def main():

    parser = ClientAParser(
        "data/raw/Patient-membership-clientA-202307.xlsx"
    )

    df = parser.read_file()

    df = parser.standardize_columns(df)

    df = convert_dates(df)

    print(df.dtypes)


if __name__ == "__main__":
    main()