import glob
import pandas as pd


def read_membership_files():

    files = glob.glob("data/raw/Patient-membership-clientA-*.xlsx")

    dfs = []

    for file in files:
        print(f"Reading {file}")
        dfs.append(pd.read_excel(file))

    return pd.concat(dfs, ignore_index=True)


def read_claim_files():

    files = glob.glob("data/raw/Patient-claim-clientA-*.xlsx")

    dfs = []

    for file in files:
        print(f"Reading {file}")
        dfs.append(pd.read_excel(file))

    return pd.concat(dfs, ignore_index=True)