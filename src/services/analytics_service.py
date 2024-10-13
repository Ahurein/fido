from datetime import datetime
from urllib.request import DataHandler
from fastapi.encoders import  jsonable_encoder

from beanie import PydanticObjectId

from src.schemas.api_response import ApiResponse, error_response
from src.schemas.transaction_create import TransactionCreateDto
from src.models.trasactions import  Transaction
from src.schemas.transaction_update import TransactionUpdateDto
from src.services.transaction_encryption_service import TransactionEncryptionService

transaction_encryption_service = TransactionEncryptionService()



class AnalyticsService:
    async def get_transaction_summary(self, user_id):
