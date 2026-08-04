def categorize_diagnosis(df):

    mapping = {
        "Diabetes mellitus": "Chronic",
        "Hypertension": "Chronic",
        "Obesity": "Chronic",
        "Acute appendicitis": "Acute"
    }

    df["diagnosis_category"] = (
        df["primary_diagnosis"]
        .map(mapping)
        .fillna("Other")
    )

    return df