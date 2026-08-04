import pandas as pd



def upsert_claims(
        existing_claims,
        incremental_claims
):

    print(
        "Existing claims:",
        len(existing_claims)
    )


    print(
        "Incremental claims:",
        len(incremental_claims)
    )



    combined = pd.concat(
        [
            existing_claims,
            incremental_claims
        ],
        ignore_index=True
    )



    if "claim_number" in combined.columns:

        combined = (
            combined
            .drop_duplicates(
                subset=[
                    "claim_number"
                ],
                keep="last"
            )
        )



    return combined.reset_index(
        drop=True
    )