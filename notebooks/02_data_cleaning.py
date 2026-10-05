import pandas as pd
import os

FILE_PATH = "data/creditcard.csv"
OUTPUT_PATH = "data/cleaned_creditcard.csv"

df = pd.read_csv(FILE_PATH)

print("\n========== BEFORE CLEANING ==========")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum().sum())

print("\n========== DUPLICATES ==========")
print("Duplicate rows:", df.duplicated().sum())

print("\n========== CLASS VALUES ==========")
print(df["Class"].value_counts())

print("\n========== INVALID CLASS VALUES ==========")
print(df[~df["Class"].isin([0, 1])].shape[0])

print("\n========== INVALID AMOUNT VALUES ==========")
print("Negative amounts:", (df["Amount"] < 0).sum())
print("Zero amounts:", (df["Amount"] == 0).sum())

print("\n========== INVALID TIME VALUES ==========")
print("Negative time:", (df["Time"] < 0).sum())

df = df.drop_duplicates()

print("\n========== AFTER DUPLICATE REMOVAL ==========")
print("Rows:", len(df))
print("Duplicates:", df.duplicated().sum())

os.makedirs("data", exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print("\n========== CLEAN DATASET SAVED ==========")
print("File:", OUTPUT_PATH)
print("Rows:", len(df))
print("Columns:", len(df.columns))