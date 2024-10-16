from datetime import datetime

from beanie import PydanticObjectId

from src.core.redis import get_redis_value, set_redis_value, delete_redis_value
from src.exceptions.exceptions import NotFoundException
from src.models.transactions import Transaction
from src.schemas.api_response import success_response, PaginatedApiResponse
from src.schemas.transaction_create import TransactionCreateDto
from src.schemas.transaction_update import TransactionUpdateDto
from src.services.transaction_encryption_service import TransactionEncryptionService
from src.utils.redis_utils import get_transactions_cache_key

transaction_encryption_service = TransactionEncryptionService()


class TransactionService:
    async def create_transaction(self, data: TransactionCreateDto, redis_instance):
        """ Create a transaction for a user """
        payload = data.model_dump()
        payload["transaction_date"] = datetime.now()
        encrypted_data = transaction_encryption_service.encrypt(payload)
        new_transaction = Transaction(**encrypted_data)
        transaction = await Transaction.create(new_transaction)
        await delete_redis_value(redis_instance, get_transactions_cache_key(transaction.user_id))
        return transaction

    async def get_transactions(self, user_id: PydanticObjectId, page, limit, redis_instance):
        """ Retrieve a paginated list of user transactions """
        cached_data = await get_redis_value(redis_instance, get_transactions_cache_key(user_id, page, limit))
        if cached_data:
            return cached_data
        total_docs = await Transaction.find({"user_id": user_id}).count()
        skip = (page - 1) * limit
        transactions = await Transaction.find({"user_id": user_id}).skip(skip).limit(limit).to_list(limit)
        decrypted_data = [transaction_encryption_service.decrypt(transaction.model_dump()) for transaction in
                          transactions]
        response = PaginatedApiResponse(total=total_docs, page=page, limit=limit, data=decrypted_data)
        await set_redis_value(redis_instance, get_transactions_cache_key(user_id,page, limit), response.model_dump(), 300)
        return response

    async def update_transaction(self, transaction_id: PydanticObjectId, update_data: TransactionUpdateDto, redis_instance):
        """ Update user transactions by transaction id """
        transaction = await self.get_transaction_entity_by_id(transaction_id)
        decrypted_transaction = transaction_encryption_service.decrypt(transaction.model_dump())
        data = {k: v for k, v in update_data.model_dump().items() if v is not None}
        payload = {**decrypted_transaction, **data}
        del payload["user_id"]
        encrypted_data = transaction_encryption_service.encrypt(payload)
        _ = await transaction.update({"$set": encrypted_data})
        await delete_redis_value(redis_instance, get_transactions_cache_key(transaction.user_id))
        return await self.get_transaction_by_id(transaction_id)

    async def get_transaction_by_id(self, transaction_id: PydanticObjectId):
        """ Get transaction by transaction id """
        transaction = await self.get_transaction_entity_by_id(transaction_id)
        return transaction_encryption_service.decrypt(transaction.model_dump())

    async def get_transaction_entity_by_id(self, transaction_id: PydanticObjectId):
        """ Get transaction entity by transaction id """
        transaction = await Transaction.get(transaction_id)
        if transaction is None:
            raise NotFoundException("Transaction not found")
        return transaction

    async def delete_transaction_by_id(self, transaction_id: PydanticObjectId, redis_instance):
        """ Delete transaction by transaction id """
        transaction = await self.get_transaction_entity_by_id(transaction_id)
        await Transaction.delete(transaction)
        await delete_redis_value(redis_instance, get_transactions_cache_key(transaction.user_id))
