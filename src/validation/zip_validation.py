def validate_zip(df):

    df["zip_code"] = df["zip_code"].astype(str)

    df = df[df["zip_code"].str.len() == 5]

    return df