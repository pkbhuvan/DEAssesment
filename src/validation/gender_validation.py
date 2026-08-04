def validate_gender(df):

    valid = ["M", "F"]

    df = df[df["gender"].isin(valid)]

    return df