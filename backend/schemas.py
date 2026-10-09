from pydantic import BaseModel, Field, field_validator, ConfigDict


class TransactionInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    transaction_id: str = Field(..., min_length=1, max_length=100)
    Time: float = Field(..., ge=0, allow_inf_nan=False)

    V1: float = Field(..., allow_inf_nan=False)
    V2: float = Field(..., allow_inf_nan=False)
    V3: float = Field(..., allow_inf_nan=False)
    V4: float = Field(..., allow_inf_nan=False)
    V5: float = Field(..., allow_inf_nan=False)
    V6: float = Field(..., allow_inf_nan=False)
    V7: float = Field(..., allow_inf_nan=False)
    V8: float = Field(..., allow_inf_nan=False)
    V9: float = Field(..., allow_inf_nan=False)
    V10: float = Field(..., allow_inf_nan=False)
    V11: float = Field(..., allow_inf_nan=False)
    V12: float = Field(..., allow_inf_nan=False)
    V13: float = Field(..., allow_inf_nan=False)
    V14: float = Field(..., allow_inf_nan=False)
    V15: float = Field(..., allow_inf_nan=False)
    V16: float = Field(..., allow_inf_nan=False)
    V17: float = Field(..., allow_inf_nan=False)
    V18: float = Field(..., allow_inf_nan=False)
    V19: float = Field(..., allow_inf_nan=False)
    V20: float = Field(..., allow_inf_nan=False)
    V21: float = Field(..., allow_inf_nan=False)
    V22: float = Field(..., allow_inf_nan=False)
    V23: float = Field(..., allow_inf_nan=False)
    V24: float = Field(..., allow_inf_nan=False)
    V25: float = Field(..., allow_inf_nan=False)
    V26: float = Field(..., allow_inf_nan=False)
    V27: float = Field(..., allow_inf_nan=False)
    V28: float = Field(..., allow_inf_nan=False)

    Amount: float = Field(..., ge=0, allow_inf_nan=False)

    @field_validator("transaction_id")
    @classmethod
    def validate_transaction_id(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Transaction ID cannot be empty")

        return value