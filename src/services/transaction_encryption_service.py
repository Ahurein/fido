from cryptography.fernet import Fernet

from src.core.config import config


class TransactionEncryptionService:
    def __init__(self):
        self.fernet = Fernet(config.FERNET_KEY)

    def encrypt(self, data: dict) -> dict:
        """ Encrypt transaction data with fernet """
        return {
            **data,
            "full_name": self.fernet.encrypt(data['full_name'].encode()).decode(),
            "transaction_type": self.fernet.encrypt(data["transaction_type"].encode()).decode()
        }

    def decrypt(self, data: dict) -> dict:
        """ Decrypt transaction data with fernet """
        return {
            **data,
            "id": str(data["id"]),
            "user_id": str(data["user_id"]),
            "full_name": self.fernet.decrypt(data["full_name"].encode()).decode(),
            "transaction_type": self.fernet.decrypt(data["transaction_type"].encode()).decode(),
            "transaction_date": data["transaction_date"].isoformat()
        }
