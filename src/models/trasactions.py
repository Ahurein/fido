from datetime import datetime
from enum import Enum

from beanie import Document
from beanie import PydanticObjectId


class TransactionType(str, Enum):
    CREDIT="credit",
    DEBIT="debit"

class Transaction(Document):
    user_id: PydanticObjectId
    full_name: str
    transaction_date: datetime
    transaction_amount: float
    transaction_type: TransactionType


    class Settings:
        name = "fido_transactions"