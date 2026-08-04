import glob
import pandas as pd


def read_membership_files():

    files = glob.glob(
        "data/raw/Patient-membership-*.xlsx"
    )

    dfs = []

    for file in files:

        print(f"Reading {file}")

        df = pd.read_excel(
            file,
            dtype=str
        )

        dfs.append(df)


    return pd.concat(
        dfs,
        ignore_index=True
    )



def read_claim_files():

    files = glob.glob(
        "data/raw/Patient-claim-*.xlsx"
    )

    dfs = []

    for file in files:

        print(f"Reading {file}")

        df = pd.read_excel(
            file,
            dtype=str
        )

        dfs.append(df)


    return pd.concat(
        dfs,
        ignore_index=True
    )