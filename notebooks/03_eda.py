import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

FILE_PATH = "data/cleaned_creditcard.csv"

df = pd.read_csv(FILE_PATH)

os.makedirs("eda_outputs", exist_ok=True)

print("\n========== EDA DATASET ==========")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\n========== CLASS DISTRIBUTION ==========")
print(df["Class"].value_counts())
print(df["Class"].value_counts(normalize=True) * 100)

print("\n========== AMOUNT STATISTICS ==========")
print(df["Amount"].describe())

print("\n========== FRAUD AMOUNT STATISTICS ==========")
print(df[df["Class"] == 1]["Amount"].describe())

print("\n========== LEGITIMATE AMOUNT STATISTICS ==========")
print(df[df["Class"] == 0]["Amount"].describe())

print("\n========== FRAUD TRANSACTION TIME ==========")
print(df[df["Class"] == 1]["Time"].describe())

print("\n========== CORRELATION WITH CLASS ==========")
correlation = df.corr(numeric_only=True)["Class"].sort_values(ascending=False)
print(correlation)


plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="Class")
plt.title("Legitimate vs Fraud Transactions")
plt.xlabel("Class")
plt.ylabel("Number of Transactions")
plt.savefig("eda_outputs/class_distribution.png")
plt.show()


plt.figure(figsize=(10, 5))
sns.histplot(data=df, x="Amount", bins=100)
plt.title("Transaction Amount Distribution")
plt.xlabel("Amount")
plt.ylabel("Frequency")
plt.xlim(0, 1000)
plt.savefig("eda_outputs/amount_distribution.png")
plt.show()


plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="Class", y="Amount")
plt.title("Transaction Amount by Class")
plt.xlabel("Class")
plt.ylabel("Amount")
plt.ylim(0, 1000)
plt.savefig("eda_outputs/amount_by_class.png")
plt.show()


plt.figure(figsize=(10, 5))
sns.histplot(data=df, x="Time", hue="Class", bins=100, element="step")
plt.title("Transaction Time Distribution")
plt.xlabel("Time")
plt.ylabel("Number of Transactions")
plt.savefig("eda_outputs/time_distribution.png")
plt.show()


plt.figure(figsize=(12, 8))
correlation_matrix = df.corr(numeric_only=True)

sns.heatmap(correlation_matrix, cmap="coolwarm", center=0)
plt.title("Feature Correlation Matrix")
plt.savefig("eda_outputs/correlation_matrix.png")
plt.show()

print("\n========== EDA COMPLETE ==========")
print("EDA graphs saved in: eda_outputs/")