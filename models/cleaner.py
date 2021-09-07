import pandas as pd
import numpy as np


def prepare(df):
    print("Replacing empty strings with nans..")
    df = df.replace(r"^\s*$", np.nan, regex=True)
    print("Converting empty lists to strings and mask them with nans..")
    df = df.mask(df.applymap(str).eq("[]"))
    for col in df:
        if (df[col].name == "id") and (df[col].dtype == "int64"):
            print("++Converting integer id to object..")
            df[col] = df[col].astype("object", errors="raise")
        if df[col].dtype == "bool":
            print("++Converting booleans to floats..")  # because of pandas
            df[col] = df[col].astype("float64", errors="raise")
        if df[col].dtype == "int64":
            print("--Converting integers to floats..")
            df[col] = df[col].astype("float64", errors="raise")
    return df


def drop_nans(df):
    print("Before:")
    print(f"dataframe rows and columns = {df.shape}")
    print(f"nans = {df.isna().sum().sum()/df.size * 100:.2f} %")
    # Drop rows where all values are Null
    df = df.dropna(how="all")
    # Drop columns where all values are Null
    df = df.dropna(how="all", axis=1)
    print("")
    print("After:")
    print(f"dataframe rows and columns = {df.shape}")
    print(f"nans = {df.isna().sum().sum()/df.size * 100:.2f} %")
    return df


def filter_columns(df):
    print(
        "Removing columns with < sqrt(N) counts and categorical columns with > sqrt(N) unique values"
    )
    for col in df:
        # print("column = ", col)
        # print(df[col].dtype)
        col_entries = df[col].count()  # excluding nans
        # print("col_entries = ", col_entries)
        poisson = np.sqrt(col_entries)
        # print("poisson = ", poisson)
        unique = df[col].nunique()
        # print(f"unique = {(unique/col_entries)*100:.2f} %")
        if col_entries < poisson:
            df.drop(col, inplace=True, axis=1)
            print(
                f"+++ Column {col} dropped because counts {col_entries} < {poisson}"
            )
        elif (df[col].dtype == "object") and (unique > poisson):
            df.drop(col, inplace=True, axis=1)
            print(
                f"--- Categorical column {col} dropped because too many unique values: {unique} over {col_entries}"
            )
    return df
