from fastapi import APIRouter, status
from beanie import PydanticObjectId

from src.schemas.transaction_create import TransactionCreateDto
from src.schemas.transaction_update import TransactionUpdateDto
from src.services.transactions_service import TransactionService

transactions_router = APIRouter()
transaction_service = TransactionService()

@transactions_router.post("", status_code=status.HTTP_201_CREATED)
async def create_user_transaction(transaction_data: TransactionCreateDto):
    transaction = await transaction_service.create_transaction(transaction_data)
    return transaction

@transactions_router.patch("/{transaction_id}", status_code=status.HTTP_200_OK)
async def update_user_transaction(transaction_id: PydanticObjectId, update_data: TransactionUpdateDto):
    return await transaction_service.update_transaction(transaction_id, update_data)

@transactions_router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_transactions(user_id: PydanticObjectId):
    transactions = await transaction_service.get_transactions(user_id)
    return transactions