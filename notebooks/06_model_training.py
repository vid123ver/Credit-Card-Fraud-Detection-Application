import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from imblearn.over_sampling import SMOTE

import joblib


FILE_PATH = "data/engineered_creditcard.csv"


print("\n========== LOADING ENGINEERED DATASET ==========")

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


print("\n========== ORIGINAL CLASS DISTRIBUTION ==========")

print("Training:")
print(y_train.value_counts())

print("\nTesting:")
print(y_test.value_counts())


print("\n========== FEATURE SCALING ==========")

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)

print("Scaling completed.")


print("\n========== APPLYING SMOTE ==========")

smote = SMOTE(
    random_state=42
)

X_train_balanced, y_train_balanced = smote.fit_resample(
    X_train_scaled,
    y_train
)

print("Before SMOTE:")
print(y_train.value_counts())

print("\nAfter SMOTE:")
print(pd.Series(y_train_balanced).value_counts())


print("\n========== TRAINING LOGISTIC REGRESSION ==========")

logistic_model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

logistic_model.fit(
    X_train_balanced,
    y_train_balanced
)

print("Logistic Regression training completed.")


print("\n========== TRAINING RANDOM FOREST ==========")

random_forest_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

random_forest_model.fit(
    X_train_balanced,
    y_train_balanced
)

print("Random Forest training completed.")


print("\n========== SAVING MODELS ==========")

joblib.dump(
    scaler,
    "models/model_scaler.pkl"
)

joblib.dump(
    logistic_model,
    "models/logistic_regression.pkl"
)

joblib.dump(
    random_forest_model,
    "models/random_forest.pkl"
)


print("Saved: models/model_scaler.pkl")
print("Saved: models/logistic_regression.pkl")
print("Saved: models/random_forest.pkl")


print("\n========== MODEL TRAINING COMPLETE ==========")