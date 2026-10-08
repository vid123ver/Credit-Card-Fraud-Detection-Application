from fastapi import FastAPI

app = FastAPI(
    title="AI-Powered Credit Card Fraud Detection API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Credit Card Fraud Detection API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }