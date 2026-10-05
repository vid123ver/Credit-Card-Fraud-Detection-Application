import pandas as pd

FILE_PATH = "data/creditcard.csv"

df = pd.read_csv(FILE_PATH)

print("\n========== DATASET SHAPE ==========")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

print("\n========== FIRST 5 ROWS ==========")
print(df.head())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== DUPLICATE ROWS ==========")
print("Duplicates:", df.duplicated().sum())

print("\n========== UNIQUE VALUES ==========")
print(df.nunique())

print("\n========== NUMERICAL SUMMARY ==========")
print(df.describe())

print("\n========== MEMORY USAGE ==========")

print(df["Class"].value_counts())
print(df["Class"].value_counts(normalize=True) * 100)
df.info()