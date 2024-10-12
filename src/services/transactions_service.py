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


class TransactionService:
    async def create_transaction(self, data: TransactionCreateDto):
        try:
            payload = data.model_dump()
            payload["transaction_date"] = datetime.now()
            encrypted_data = transaction_encryption_service.encrypt(payload)
            new_transaction = Transaction(**encrypted_data)
            transaction = await Transaction.create(new_transaction)
            return transaction
        except Exception as e:
            print(e)
            return error_response()


    async def get_transactions(self, user_id: PydanticObjectId):
        try:
            transactions = await Transaction.find(Transaction.user_id==user_id).to_list()
            print(len(transactions))
            decrypted_data = [transaction_encryption_service.decrypt(transaction.model_dump()) for transaction in transactions]
            return decrypted_data
        except Exception as e:
            return error_response()

    async def update_transaction(self, transaction_id: PydanticObjectId, update_data: TransactionUpdateDto):
        try:
            transaction = await self.get_transaction_by_id(transaction_id)
            decrypted_transaction = transaction_encryption_service.decrypt(transaction.model_dump())
            data = {k:v for k, v in update_data.model_dump().items() if v is not None}
            payload = {**decrypted_transaction, **data}
            del payload["user_id"]
            encrypted_data = transaction_encryption_service.encrypt(payload)
            _ = await transaction.update({"$set": encrypted_data})
            return await  self.get_transaction_by_id(transaction_id)
        except Exception as e:
            print(e)
            return error_response()


    async def get_transaction_by_id(self, transaction_id: PydanticObjectId):
        transaction = await Transaction.get(transaction_id)
        if transaction is None:
            return error_response("Transaction not found", 404)
        return transaction_encryption_service.decrypt(transaction.model_dump())

    async def delete_transaction_by_id(self, transaction_id: PydanticObjectId):
        transaction = await self.get_transaction_by_id(transaction_id)
        await Transaction.delete(transaction)