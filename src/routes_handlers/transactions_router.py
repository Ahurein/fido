from fastapi import APIRouter, status, Depends
from beanie import PydanticObjectId

from src.core.redis import get_redis
from src.schemas.api_response import success_response
from src.schemas.transaction_create import TransactionCreateDto
from src.schemas.transaction_update import TransactionUpdateDto
from src.services.transactions_service import TransactionService

transactions_router = APIRouter()
transaction_service = TransactionService()


@transactions_router.post("", status_code=status.HTTP_201_CREATED)
async def create_user_transaction(transaction_data: TransactionCreateDto, redis_instance=Depends(get_redis)):
    transaction = await transaction_service.create_transaction(transaction_data, redis_instance)
    return success_response(transaction)


@transactions_router.patch("/{transaction_id}", status_code=status.HTTP_200_OK)
async def update_user_transaction(transaction_id: PydanticObjectId, update_data: TransactionUpdateDto,
                                  redis_instance=Depends(get_redis)):
    transaction = await transaction_service.update_transaction(transaction_id, update_data, redis_instance)
    return success_response(transaction)


@transactions_router.get("/{transaction_id}", status_code=status.HTTP_200_OK)
async def get_transaction_by_id(transaction_id: PydanticObjectId):
    transaction = await transaction_service.get_transaction_by_id(transaction_id)
    return success_response(transaction)


@transactions_router.delete("/{transaction_id}", status_code=status.HTTP_200_OK)
async def delete_transaction_by_id(transaction_id: PydanticObjectId, redis_instance=Depends(get_redis)):
    await transaction_service.delete_transaction_by_id(transaction_id, redis_instance)
    return success_response(message="Transaction deleted successfully")


@transactions_router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_transactions(user_id: PydanticObjectId, redis_instance=Depends(get_redis)):
    transactions = await transaction_service.get_transactions(user_id, redis_instance)
    return success_response(transactions)
