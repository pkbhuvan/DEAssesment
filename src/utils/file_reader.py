import glob
import pandas as pd



def read_membership_files():

    files = glob.glob(
        "data/raw/Patient-membership-*.xlsx"
    )


    if not files:
        raise FileNotFoundError(
            "No membership files found"
        )


    dfs=[]


    for file in files:

        print(f"Reading {file}")

        dfs.append(
            pd.read_excel(
                file,
                dtype=str
            )
        )


    return pd.concat(
        dfs,
        ignore_index=True
    )




def read_claim_files():

    files = glob.glob(
        "data/raw/Patient-claim-*.xlsx"
    )


    if not files:
        raise FileNotFoundError(
            "No claim files found"
        )


    dfs=[]


    for file in files:

        print(f"Reading {file}")

        dfs.append(
            pd.read_excel(
                file,
                dtype=str
            )
        )


    return pd.concat(
        dfs,
        ignore_index=True
    )





# =========================================
# Incremental claim load
# =========================================


def read_incremental_claim_files():

    files = glob.glob(
        "data/raw/Patient-claim-clientA-*.xlsx"
    )


    if not files:

        raise FileNotFoundError(
            "No incremental claim file found"
        )


    # pick latest file
    files = sorted(files)


    incremental_file = files[-1]


    print(
        f"Reading incremental claim file: {incremental_file}"
    )


    return pd.read_excel(
        incremental_file,
        dtype=str
    )