import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("MONGODB_DATABASE", "fraud_detection")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is not set in .env")

client = MongoClient(MONGODB_URI)

db = client[DATABASE_NAME]

transactions_collection = db["transactions"]
alerts_collection = db["alerts"]
reviews_collection = db["reviews"]
model_metadata_collection = db["model_metadata"]


def test_database_connection():
    client.admin.command("ping")
    return True