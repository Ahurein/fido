from datetime import datetime

from beanie import PydanticObjectId

from src.core.redis import get_redis_value, set_redis_value, delete_redis_value
from src.exceptions.exceptions import NotFoundException
from src.models.trasactions import Transaction
from src.schemas.api_response import success_response
from src.schemas.transaction_create import TransactionCreateDto
from src.schemas.transaction_update import TransactionUpdateDto
from src.services.transaction_encryption_service import TransactionEncryptionService
from src.utils.redis_utils import get_transactions_cache_key

transaction_encryption_service = TransactionEncryptionService()


class TransactionService:
    async def create_transaction(self, data: TransactionCreateDto, redis_instance):
        payload = data.model_dump()
        payload["transaction_date"] = datetime.now()
        encrypted_data = transaction_encryption_service.encrypt(payload)
        new_transaction = Transaction(**encrypted_data)
        transaction = await Transaction.create(new_transaction)
        await delete_redis_value(redis_instance, get_transactions_cache_key(transaction.user_id))
        return transaction

    async def get_transactions(self, user_id: PydanticObjectId, redis_instance):
        cached_data = await get_redis_value(redis_instance, get_transactions_cache_key(user_id))
        if cached_data:
            return cached_data
        transactions = await Transaction.find(Transaction.user_id == user_id).to_list()
        decrypted_data = [transaction_encryption_service.decrypt(transaction.model_dump()) for transaction in
                          transactions]
        await set_redis_value(redis_instance, get_transactions_cache_key(user_id), decrypted_data, 600)
        return decrypted_data

    async def update_transaction(self, transaction_id: PydanticObjectId, update_data: TransactionUpdateDto, redis_instance):
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
        transaction = await self.get_transaction_entity_by_id(transaction_id)
        return transaction_encryption_service.decrypt(transaction.model_dump())

    async def get_transaction_entity_by_id(self, transaction_id: PydanticObjectId):
        transaction = await Transaction.get(transaction_id)
        if transaction is None:
            raise NotFoundException("Transaction not found")
        return transaction

    async def delete_transaction_by_id(self, transaction_id: PydanticObjectId, redis_instance):
        transaction = await self.get_transaction_entity_by_id(transaction_id)
        await Transaction.delete(transaction)
        await delete_redis_value(redis_instance, get_transactions_cache_key(transaction.user_id))
