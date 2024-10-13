from beanie import PydanticObjectId
from fastapi import APIRouter, status, Query

from src.models.trasactions import Transaction
from src.schemas.api_response import error_response
from src.schemas.transactions_stats_query import TransactionStatsDto

analytics_router = APIRouter()

@analytics_router.get("/transactions/{user_id}", status_code=status.HTTP_200_OK)
async def get_transaction_stats(user_id: PydanticObjectId, query: TransactionStatsDto = Query()):
    match = dict(user_id = user_id)

    if query.start_date and query.end_date:
        match["transaction_date"] = {"$gte": query.start_date, "$lte": query.end_date}

    aggregate_pipeline = [
        {
            "$match": match
        },
        {
            "$group": {
                "_id": {"day": {"$dateToString": {"format": "%Y-%m-%d", "date": "$transaction_date"}}},
                "transaction_count": {"$sum": 1},
                "total_transaction": {"$sum": "$transaction_amount"},
                "average_transaction": {"$avg": "$transaction_amount"},
            }
        },
        {
            "$sort": {"transaction_count": -1}
        },
        {
            "$limit": 1
        }
    ]
    response = await Transaction.aggregate(aggregate_pipeline).to_list()
    if len(response) == 0:
        return error_response("User does not have any transactions")
    return {
        "highest_transaction_day": response[0]["_id"]["day"],
        "average_transaction": response[0]["average_transaction"],
        "total_transaction": response[0]["total_transaction"]
    }