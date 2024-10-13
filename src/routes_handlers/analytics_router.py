from beanie import PydanticObjectId
from fastapi import APIRouter, status, Query, Depends

from src.core.redis import get_redis
from src.schemas.api_response import success_response
from src.schemas.transactions_stats_query import TransactionStatsDto
from src.services.analytics_service import AnalyticsService

analytics_router = APIRouter()

analytics_service = AnalyticsService()

@analytics_router.get("/transactions/{user_id}", status_code=status.HTTP_200_OK)
async def get_transaction_stats(user_id: PydanticObjectId, query: TransactionStatsDto = Query(), redis_instance = Depends(get_redis)):
    stats = await analytics_service.get_transaction_summary(user_id, query, redis_instance)
    return success_response(stats)
