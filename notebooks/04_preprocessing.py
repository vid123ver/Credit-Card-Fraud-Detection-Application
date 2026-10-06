import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


FILE_PATH = "data/cleaned_creditcard.csv"

TRAIN_FEATURES_PATH = "data/X_train.csv"
TEST_FEATURES_PATH = "data/X_test.csv"
TRAIN_TARGET_PATH = "data/y_train.csv"
TEST_TARGET_PATH = "data/y_test.csv"

SCALER_PATH = "models/scaler.pkl"


print("\n========== LOADING CLEAN DATASET ==========")

df = pd.read_csv(FILE_PATH)

print("Rows:", len(df))
print("Columns:", len(df.columns))


print("\n========== SEPARATING FEATURES AND TARGET ==========")

X = df.drop("Class", axis=1)
y = df["Class"]

print("Feature shape:", X.shape)
print("Target shape:", y.shape)


print("\n========== TRAIN TEST SPLIT ==========")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


print("\n========== CLASS DISTRIBUTION ==========")

print("Training:")
print(y_train.value_counts())
print(y_train.value_counts(normalize=True) * 100)

print("\nTesting:")
print(y_test.value_counts())
print(y_test.value_counts(normalize=True) * 100)


print("\n========== FEATURE SCALING ==========")

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Scaling completed.")


print("\n========== CHECKING SCALED DATA ==========")

print("Training mean:")
print(np.mean(X_train_scaled, axis=0).round(4))

print("\nTraining standard deviation:")
print(np.std(X_train_scaled, axis=0).round(4))


print("\n========== SAVING PREPROCESSED DATA ==========")

os.makedirs("models", exist_ok=True)

pd.DataFrame(
    X_train_scaled,
    columns=X.columns
).to_csv(TRAIN_FEATURES_PATH, index=False)

pd.DataFrame(
    X_test_scaled,
    columns=X.columns
).to_csv(TEST_FEATURES_PATH, index=False)

y_train.to_csv(TRAIN_TARGET_PATH, index=False)
y_test.to_csv(TEST_TARGET_PATH, index=False)

joblib.dump(scaler, SCALER_PATH)


print("Saved:", TRAIN_FEATURES_PATH)
print("Saved:", TEST_FEATURES_PATH)
print("Saved:", TRAIN_TARGET_PATH)
print("Saved:", TEST_TARGET_PATH)
print("Saved:", SCALER_PATH)


print("\n========== PREPROCESSING COMPLETE ==========")