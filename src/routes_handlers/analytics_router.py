from beanie import PydanticObjectId
from fastapi import APIRouter, status, Query, Depends

from src.core.redis import get_redis, get_redis_value, set_redis_value
from src.models.trasactions import Transaction
from src.schemas.api_response import error_response
from src.schemas.transactions_stats_query import TransactionStatsDto
from src.utils.redis_utils import get_analytics_cache_key

analytics_router = APIRouter()

@analytics_router.get("/transactions/{user_id}", status_code=status.HTTP_200_OK)
async def get_transaction_stats(user_id: PydanticObjectId, query: TransactionStatsDto = Query(), redis_instance = Depends(get_redis)):
    cached_data = await get_redis_value(redis_instance, get_analytics_cache_key(user_id))
    if cached_data:
        return cached_data
    match = dict(user_id = user_id)
    if query.start_date and query.end_date:
        match["transaction_date"] = {"$gte": query.start_date, "$lte": query.end_date}

    total_avg_pipeline = [
        {
            "$match": match
        },
        {
            "$group": {
                "_id": None,
                "total_transaction": {"$sum": "$transaction_amount"},
                "average_transaction": {"$avg": "$transaction_amount"},
            }
        }
    ]

    highest_day_pipeline = [
        {
            "$match": match
        },
        {
            "$group": {
                "_id": {"day": {"$dateToString": {"format": "%Y-%m-%d", "date": "$transaction_date"}}},
                "transaction_count": {"$sum": 1}
            }
        },
        {
            "$sort": {"transaction_count": -1}
        },
        {
            "$limit": 1
        }
    ]

    total_avg_response = await Transaction.aggregate(total_avg_pipeline).to_list()
    highest_day_response = await Transaction.aggregate(highest_day_pipeline).to_list()

    if len(total_avg_response) == 0 or len(highest_day_response) ==0:
        return error_response("User does not have any transactions")
    summary = {
        "highest_transaction_day": highest_day_response[0]["_id"]["day"],
        "average_transaction": total_avg_response[0]["average_transaction"],
        "total_transaction": total_avg_response[0]["total_transaction"]
    }
    await set_redis_value(redis_instance, get_analytics_cache_key(user_id), summary, ttl=600)
    return summary