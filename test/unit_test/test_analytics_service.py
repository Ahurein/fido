import json
from datetime import datetime, timedelta

import pytest

from src.exceptions.exceptions import NotFoundException
from src.schemas.transactions_stats_query import TransactionStatsDto
from test.conftest import transaction_two_data



class TestAnalyticsService:
    @pytest.mark.asyncio
    async def test_when_no_date_range_return_stats(self, transaction_service_to_test, mock_redis_instance,
                                                    mock_encryption_service,
                                                    encrypted_data, transaction_data, setup_db, transaction_two_data,
                                                    analytics_service_to_test):
        """Get all user transactions statics when no date range is given and not cached"""
        query = TransactionStatsDto()
        mock_encryption_service.encrypt.return_value = encrypted_data
        await transaction_service_to_test.create_transaction(transaction_data, mock_redis_instance)
        await transaction_service_to_test.create_transaction(transaction_two_data, mock_redis_instance)
        mock_redis_instance.get.return_value = None

        stats = await analytics_service_to_test.get_transaction_summary(transaction_data.user_id, query,
                                                                        mock_redis_instance)

        assert isinstance(stats, dict)
        assert stats["highest_transaction_day"] == '2024-10-13'
        assert stats["average_transaction"] == 22.5
        assert stats["total_transaction"] == 45.0


    @pytest.mark.asyncio
    async def test_when_date_range_return_stats(self, transaction_service_to_test, mock_redis_instance,
                                                    mock_encryption_service,
                                                    encrypted_data, transaction_data, setup_db, transaction_two_data,
                                                    analytics_service_to_test):
        """Get all user transactions statics when given a date range with no transactions and not cached"""

        query = TransactionStatsDto()
        now = datetime.now()
        query.start_date = now - timedelta(minutes=10)
        query.end_date = now - timedelta(minutes=5)
        mock_encryption_service.encrypt.return_value = encrypted_data
        await transaction_service_to_test.create_transaction(transaction_data, mock_redis_instance)
        await transaction_service_to_test.create_transaction(transaction_two_data, mock_redis_instance)
        mock_redis_instance.get.return_value = None

        with pytest.raises(NotFoundException):
            await analytics_service_to_test.get_transaction_summary(transaction_data.user_id, query,
                                                                    mock_redis_instance)