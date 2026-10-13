from pathlib import Path
import json

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

EVALUATION_FILE = BASE_DIR / "data" / "model_evaluation_results.csv"
METADATA_FILE = BASE_DIR / "models" / "model_metadata.json"


def get_model_performance():
    if not EVALUATION_FILE.exists():
        raise FileNotFoundError(
            "Model evaluation results file not found. "
            "Run Chapter 7 evaluation first."
        )

    df = pd.read_csv(EVALUATION_FILE)

    # Convert NaN values to JSON-compatible None values.
    records = json.loads(df.to_json(orient="records"))

    return {
        "total_models": len(records),
        "models": records
    }


def get_model_metadata():
    if not METADATA_FILE.exists():
        raise FileNotFoundError(
            "Model metadata file not found."
        )

    with open(METADATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)