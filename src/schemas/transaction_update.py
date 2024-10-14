from pydantic import BaseModel, Field, confloat
from typing import Optional

from src.models.transactions import TransactionType


class TransactionUpdateDto(BaseModel):
    full_name: Optional[str] = None
    transaction_amount: Optional[confloat(ge=0.0)] = None
    transaction_type: Optional[TransactionType] = None