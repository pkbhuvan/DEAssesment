def handle_missing_values(df):

    df["ethnicity"] = df["ethnicity"].fillna("Unknown")

    df["state"] = df["state"].fillna("Unknown")

    return df