from datetime import datetime
from urllib.request import DataHandler
from fastapi.encoders import  jsonable_encoder

from beanie import PydanticObjectId

from src.schemas.api_response import ApiResponse, error_response
from src.schemas.transaction_create import TransactionCreateDto
from src.models.trasactions import  Transaction
from src.schemas.transaction_update import TransactionUpdateDto


class TransactionService:
    async def create_transaction(self, data: TransactionCreateDto):
        try:
            payload = data.model_dump()
            payload["transaction_date"] = datetime.now()
            print(payload)
            new_transaction = Transaction(**payload)
            transaction = await Transaction.create(new_transaction)
            return transaction
        except Exception as e:
            print(e)
            return error_response()


    async def get_transactions(self, user_id: PydanticObjectId):
        try:
            transactions = await Transaction.find(Transaction.user_id==user_id).to_list()
            return transactions
        except Exception as e:
            print(e)
            return error_response()

    async def update_transaction(self, transaction_id: PydanticObjectId, update_data: TransactionUpdateDto):
        try:
            transaction = await self.get_transaction_by_id(transaction_id)
            payload = jsonable_encoder(update_data)
            data = {k:v for k, v in payload.items() if v is not None}
            _ = await transaction.update({"$set":data})
            return await  self.get_transaction_by_id(transaction_id)
        except Exception as e:
            print(e)
            return error_response()


    async def get_transaction_by_id(self, transaction_id: PydanticObjectId):
        transaction = await Transaction.get(transaction_id)
        if transaction is None:
            return error_response("Transaction not found", 404)
        return transaction