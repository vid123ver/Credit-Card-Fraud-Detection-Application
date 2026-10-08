import json
import joblib
from datetime import datetime

MODEL_PATH = "models/random_forest.pkl"
VERSIONED_MODEL_PATH = "models/random_forest_v1.pkl"
SCALER_PATH = "models/model_scaler.pkl"
RESULTS_PATH = "data/model_evaluation_results.csv"
METADATA_PATH = "models/model_metadata.json"

print("\n========== LOADING FINAL MODEL ==========")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

print("Random Forest model loaded.")
print("Scaler loaded.")

print("\n========== SAVING VERSIONED MODEL ==========")

joblib.dump(model, VERSIONED_MODEL_PATH)

print("Model saved as:", VERSIONED_MODEL_PATH)

print("\n========== LOADING EVALUATION RESULTS ==========")

import pandas as pd

results = pd.read_csv(RESULTS_PATH)

random_forest_result = results[
    results["Model"] == "RANDOM FOREST"
].iloc[0]

print("Random Forest evaluation results loaded.")

print("\n========== CREATING MODEL METADATA ==========")

metadata = {
    "model_name": "Random Forest",
    "model_version": "v1",
    "model_file": VERSIONED_MODEL_PATH,
    "scaler_file": SCALER_PATH,
    "training_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "precision": float(random_forest_result["Precision"]),
    "recall": float(random_forest_result["Recall"]),
    "f1_score": float(random_forest_result["F1 Score"]),
    "roc_auc": float(random_forest_result["ROC-AUC"]),
    "pr_auc": float(random_forest_result["PR-AUC"]),
    "threshold": 0.50
}

with open(METADATA_PATH, "w") as file:
    json.dump(metadata, file, indent=4)

print("Metadata saved as:", METADATA_PATH)

print("\n========== MODEL INFORMATION ==========")

print("Model:", metadata["model_name"])
print("Version:", metadata["model_version"])
print("Training Date:", metadata["training_date"])
print("Precision:", round(metadata["precision"], 4))
print("Recall:", round(metadata["recall"], 4))
print("F1 Score:", round(metadata["f1_score"], 4))
print("ROC-AUC:", round(metadata["roc_auc"], 4))
print("PR-AUC:", round(metadata["pr_auc"], 4))
print("Threshold:", metadata["threshold"])

print("\n========== CHAPTER 8 COMPLETE ==========")