from src.core.redis import get_redis_value, set_redis_value
from src.exceptions.exceptions import NotFoundException
from src.models.transactions import Transaction
from src.schemas.transactions_stats_query import TransactionStatsDto
from src.services.transaction_encryption_service import TransactionEncryptionService
from src.utils.redis_utils import get_analytics_cache_key

transaction_encryption_service = TransactionEncryptionService()



class AnalyticsService:
    async def get_transaction_summary(self, user_id, query: TransactionStatsDto, redis_instance):
        """ Get user transaction summary using mongodb aggregate for performance"""
        cached_data = await get_redis_value(redis_instance, get_analytics_cache_key(user_id))
        if cached_data:
            return cached_data
        match = dict(user_id=user_id)
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

        if not total_avg_response or not highest_day_response:
            raise NotFoundException("User does not have any transactions or in the specified range")

        summary = {
            "highest_transaction_day": highest_day_response[0]["_id"]["day"],
            "average_transaction": total_avg_response[0]["average_transaction"],
            "total_transaction": total_avg_response[0]["total_transaction"]
        }
        await set_redis_value(redis_instance, get_analytics_cache_key(user_id), summary, ttl=600)
        return summary