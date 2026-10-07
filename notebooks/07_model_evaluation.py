import pandas as pd
import numpy as np
import joblib

from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score
)


DATA_PATH = "data/engineered_creditcard.csv"

LOGISTIC_MODEL_PATH = "models/logistic_regression.pkl"
RANDOM_FOREST_MODEL_PATH = "models/random_forest.pkl"

THRESHOLD = 0.50


print("\n========== LOADING DATA ==========")

df = pd.read_csv(DATA_PATH)

X = df.drop("Class", axis=1)
y = df["Class"]

print("Dataset shape:", X.shape)


print("\n========== RECREATING TEST SPLIT ==========")

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Test samples:", len(X_test))
print("Actual test classes:")
print(y_test.value_counts())


print("\n========== LOADING SCALER ==========")

scaler = joblib.load("models/model_scaler.pkl")

X_test_scaled = scaler.transform(X_test)

print("Test data scaled.")


print("\n========== LOADING MODELS ==========")

logistic_model = joblib.load(LOGISTIC_MODEL_PATH)

random_forest_model = joblib.load(
    RANDOM_FOREST_MODEL_PATH
)

print("Models loaded successfully.")


def evaluate_model(model, model_name):

    print("\n")
    print("=" * 60)
    print(model_name)
    print("=" * 60)

    probabilities = model.predict_proba(X_test_scaled)[:, 1]

    predictions = (
        probabilities >= THRESHOLD
    ).astype(int)

    cm = confusion_matrix(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities
    )

    pr_auc = average_precision_score(
        y_test,
        probabilities
    )

    print("\n========== CONFUSION MATRIX ==========")

    print(cm)

    print("\n========== CLASSIFICATION REPORT ==========")

    print(
        classification_report(
            y_test,
            predictions,
            target_names=[
                "Legitimate",
                "Fraud"
            ],
            zero_division=0
        )
    )

    print("\n========== METRICS ==========")

    print("Precision:", round(precision, 4))
    print("Recall:", round(recall, 4))
    print("F1 Score:", round(f1, 4))
    print("ROC-AUC:", round(roc_auc, 4))
    print("PR-AUC:", round(pr_auc, 4))

    return {
        "Model": model_name,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC-AUC": roc_auc,
        "PR-AUC": pr_auc
    }


logistic_results = evaluate_model(
    logistic_model,
    "LOGISTIC REGRESSION"
)


random_forest_results = evaluate_model(
    random_forest_model,
    "RANDOM FOREST"
)


print("\n")
print("=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

results = pd.DataFrame(
    [
        logistic_results,
        random_forest_results
    ]
)

print(
    results.to_string(
        index=False
    )
)


results.to_csv(
    "data/model_evaluation_results.csv",
    index=False
)

print("\nSaved: data/model_evaluation_results.csv")

print("\n========== EVALUATION COMPLETE ==========")