from datetime import datetime
from enum import Enum
from beanie import PydanticObjectId

from beanie import Indexed, Document
from src.models.base_model import DocumentBaseModel


class TransactionType(str, Enum):
    CREDIT="credit",
    DEBIT="debit"

class Transaction(Document):
    user_id: PydanticObjectId
    full_name: str
    transaction_date: datetime
    transaction_amount: float
    transaction_type: str


    class Settings:
        name = "fido_transactions"