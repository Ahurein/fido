from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import config
from src.models.transactions import Transaction
from src.models.transactions import TransactionType
from src.schemas.transaction_create import TransactionCreateDto
from src.schemas.transactions_stats_query import TransactionStatsDto
from src.services.analytics_service import AnalyticsService
from src.services.transactions_service import TransactionService

redis_instance = AsyncMock()


@pytest.fixture
def mock_redis_instance():
    return redis_instance


@pytest.fixture
def mock_encryption_service():
    with patch("src.services.transaction_encryption_service") as mock_service:
        yield mock_service


@pytest.fixture
def transaction_service_to_test(mock_encryption_service):
    return TransactionService()

@pytest.fixture
def analytics_service_to_test(mock_encryption_service):
    return AnalyticsService()


@pytest.fixture
def transaction_data():
    return TransactionCreateDto(
        user_id="65e25a6bfb249dcbfbf00b93",
        transaction_type="credit",
        transaction_amount=10.0,
        full_name="Ahurein"
    )

@pytest.fixture
def transaction_two_data():
    return TransactionCreateDto(
        user_id="65e25a6bfb249dcbfbf00b93",
        transaction_type="credit",
        transaction_amount=35.0,
        full_name="Ahurein"
    )

@pytest.fixture
def decrypted_data():
    return {
            "user_id": "65e25a6bfb249dcbfbf00b93",
            "full_name": "Ahurein",
            "transaction_amount": 52,
            "transaction_type": TransactionType.CREDIT,
            "transaction_date": datetime.now()
        }


@pytest.fixture
def encrypted_data():
    return {
            "user_id": "65e25a6bfb249dcbfbf00b93",
            "full_name": "Ahurein",
            "transaction_amount": 52,
            "transaction_type": TransactionType.CREDIT,
            "transaction_date": datetime.now()
        }

@pytest.fixture
def transactions_stats_query():
    return TransactionStatsDto()


@pytest_asyncio.fixture
async def setup_db():
    client = AsyncIOMotorClient(config.DB_URI)
    db = client["test_db"]
    await init_beanie(database=db, document_models=[Transaction])
    yield db
    await client.drop_database("test_db")
