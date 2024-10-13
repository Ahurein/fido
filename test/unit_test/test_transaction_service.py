import json
from datetime import datetime

import pytest

from src.exceptions.exceptions import NotFoundException


class TestTransactionService:
    @pytest.mark.asyncio
    async def test_create_transaction(self, transaction_service_to_test, mock_redis_instance, mock_encryption_service,
                                      encrypted_data, transaction_data,setup_db):
        """Test creating a new transaction for a user"""

        mock_encryption_service.encrypt.return_value = encrypted_data

        transaction = await transaction_service_to_test.create_transaction(transaction_data, mock_redis_instance)

        assert transaction.user_id == transaction_data.user_id
        assert transaction.transaction_amount == transaction_data.transaction_amount

    @pytest.mark.asyncio
    async def test_when_user_id_get_user_transactions(self, transaction_service_to_test, mock_redis_instance,
                                                      mock_encryption_service, transaction_data, transaction_two_data, decrypted_data, setup_db):
        """Test the retrieval of transactions for a given user"""

        await transaction_service_to_test.create_transaction(transaction_data, mock_redis_instance)
        await transaction_service_to_test.create_transaction(transaction_two_data, mock_redis_instance)

        mock_encryption_service.decrypt.return_value = decrypted_data
        mock_redis_instance.get.return_value = None

        transactions = await transaction_service_to_test.get_transactions(transaction_data.user_id,
                                                                          mock_redis_instance)
        assert transactions is not None
        assert len(transactions) == 2
        assert transactions[0]["user_id"] == str(transaction_data.user_id)

    @pytest.mark.asyncio
    async def test_when_transaction_id_get_transaction(self, transaction_service_to_test, mock_redis_instance,
                                                       mock_encryption_service, transaction_data, setup_db):
        """Test the retrieval of transaction by transaction id"""

        new_transaction = await transaction_service_to_test.create_transaction(transaction_data,
                                                                               mock_redis_instance)

        transaction = await transaction_service_to_test.get_transaction_by_id(new_transaction.id)

        assert transaction is not None
        assert transaction["user_id"] == str(new_transaction.user_id)

    @pytest.mark.asyncio
    async def test_when_invalid_transaction_id_return_transaction(self, transaction_service_to_test,
                                                                  mock_redis_instance, mock_encryption_service,
                                                                  setup_db, transaction_data):
        """Test the retrieval of transaction by providing invalid transaction id"""
        new_transaction = await transaction_service_to_test.create_transaction(transaction_data,
                                                                               mock_redis_instance)

        with pytest.raises(NotFoundException):
            await transaction_service_to_test.get_transaction_by_id(transaction_data.user_id)

    @pytest.mark.asyncio
    async def test_when_updated_return_updated_data(self, transaction_service_to_test, mock_redis_instance,
                                                    mock_encryption_service, transaction_data, setup_db):
        """Test updating transaction by transaction id"""

        new_transaction_amount = 50.0
        new_transaction = await transaction_service_to_test.create_transaction(transaction_data,
                                                                               mock_redis_instance)

        new_transaction.transaction_amount = new_transaction_amount
        await new_transaction.save()

        transaction = await transaction_service_to_test.get_transaction_by_id(new_transaction.id)

        assert transaction is not None
        assert transaction["transaction_amount"] != transaction_data.transaction_amount
        assert transaction["transaction_amount"] == new_transaction_amount

    @pytest.mark.asyncio
    async def test_when_deleted_raise_not_found(self, transaction_service_to_test, mock_redis_instance,
                                                mock_encryption_service,transaction_data, setup_db):
        """Test deleting transaction by transaction id"""

        new_transaction = await transaction_service_to_test.create_transaction(transaction_data,
                                                                               mock_redis_instance)

        _ = await transaction_service_to_test.delete_transaction_by_id(new_transaction.id, mock_redis_instance)

        with pytest.raises(NotFoundException):
            await transaction_service_to_test.get_transaction_by_id(new_transaction.id)

    @pytest.mark.asyncio
    async def test_when_cached_return_user_transactions(self, transaction_service_to_test, mock_redis_instance,
                                                        mock_encryption_service, transaction_data, decrypted_data, setup_db):
        """Test the retrieval of transactions for a given user from redis cache."""

        await transaction_service_to_test.create_transaction(transaction_data, mock_redis_instance)
        await transaction_service_to_test.create_transaction(transaction_data, mock_redis_instance)

        mock_encryption_service.decrypt.return_value = decrypted_data
        mock_redis_instance.get.return_value = json.dumps([
            {
                "user_id": str(transaction_data.user_id),
                "full_name": transaction_data.full_name,
                "transaction_amount": transaction_data.transaction_amount,
                "transaction_type": transaction_data.transaction_type,
                "transaction_date": datetime.now().isoformat()
            }
        ])

        transactions = await transaction_service_to_test.get_transactions(transaction_data.user_id,
                                                                          mock_redis_instance)
        assert len(transactions) == 1
        assert transactions[0]["user_id"] == str(transaction_data.user_id)
        assert transactions[0]["transaction_amount"] == transaction_data.transaction_amount

    @pytest.mark.asyncio
    async def test_when_id_return_transaction_entity(self, transaction_service_to_test, mock_redis_instance,
                                                       mock_encryption_service, transaction_data, setup_db):
        """Test the retrieval of transaction by transaction id that return transaction entity"""

        new_transaction = await transaction_service_to_test.create_transaction(transaction_data,
                                                                               mock_redis_instance)

        transaction = await transaction_service_to_test.get_transaction_entity_by_id(new_transaction.id)

        assert transaction is not None
        assert transaction.user_id == new_transaction.user_id