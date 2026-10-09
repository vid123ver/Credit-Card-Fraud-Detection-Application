from pydantic import BaseModel, Field

from backend.schemas import TransactionInput


class BatchPredictionInput(BaseModel):
    transactions: list[TransactionInput] = Field(
        ...,
        min_length=1,
        max_length=100
    )