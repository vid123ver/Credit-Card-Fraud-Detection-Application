import pandas as pd
import numpy as np


FILE_PATH = "data/cleaned_creditcard.csv"
OUTPUT_PATH = "data/engineered_creditcard.csv"


print("\n========== LOADING CLEAN DATASET ==========")

df = pd.read_csv(FILE_PATH)

print("Rows:", len(df))
print("Columns:", len(df.columns))


print("\n========== CREATING TIME FEATURE ==========")

df["Time_hours"] = df["Time"] / 3600

print("Time_hours created.")


print("\n========== CREATING AMOUNT FEATURE ==========")

df["Amount_log"] = np.log1p(df["Amount"])

print("Amount_log created.")


print("\n========== IDENTIFYING V FEATURES ==========")

v_columns = [f"V{i}" for i in range(1, 29)]

print("Number of V features:", len(v_columns))


print("\n========== CREATING V FEATURE STATISTICS ==========")

df["V_mean"] = df[v_columns].mean(axis=1)

df["V_std"] = df[v_columns].std(axis=1)

df["V_abs_mean"] = df[v_columns].abs().mean(axis=1)

df["V_max"] = df[v_columns].max(axis=1)

df["V_min"] = df[v_columns].min(axis=1)

print("V feature statistics created.")


print("\n========== FEATURE LIST ==========")

print(df.columns.tolist())


print("\n========== FEATURE ENGINEERING SUMMARY ==========")

print("Original columns:", 31)
print("New features:", len(df.columns) - 31)
print("Final columns:", len(df.columns))


print("\n========== NEW FEATURE STATISTICS ==========")

print(
    df[
        [
            "Time_hours",
            "Amount_log",
            "V_mean",
            "V_std",
            "V_abs_mean",
            "V_max",
            "V_min"
        ]
    ].describe()
)


print("\n========== CHECKING MISSING VALUES ==========")

print(
    df[
        [
            "Time_hours",
            "Amount_log",
            "V_mean",
            "V_std",
            "V_abs_mean",
            "V_max",
            "V_min"
        ]
    ].isnull().sum()
)


print("\n========== SAVING ENGINEERED DATASET ==========")

df.to_csv(OUTPUT_PATH, index=False)

print("Saved:", OUTPUT_PATH)


print("\n========== FEATURE ENGINEERING COMPLETE ==========")