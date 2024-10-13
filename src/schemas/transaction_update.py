from pydantic import BaseModel, Field, confloat
from typing import Optional

from src.models.transactions import TransactionType


class TransactionUpdateDto(BaseModel):
    full_name: Optional[str] = None
    transaction_amount: Optional[confloat(ge=0.0)] = None
    transaction_type: Optional[TransactionType] = None

    # @field_validator('full_name', mode='before')
    # def check_full_name(cls, value):
    #     if value is not None and value.strip() == "":
    #         raise ValueError("full_name cannot be an empty string")
    #     return value
    #
    # @field_validator('transaction_amount')
    # def check_transaction_amount(cls, value):
    #     if value <= 0:
    #         raise ValueError("transaction_amount must be a positive number")
    #     return value