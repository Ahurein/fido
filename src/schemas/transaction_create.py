from pydantic import BaseModel, confloat
from beanie import Indexed, PydanticObjectId
from src.models.transactions import TransactionType
from datetime import datetime


class TransactionCreateDto(BaseModel):
    user_id: PydanticObjectId
    full_name: str
    transaction_amount: confloat(ge=0.0)
    transaction_type: TransactionType