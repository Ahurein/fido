from motor.motor_asyncio import  AsyncIOMotorClient
from beanie import init_beanie
from src.core.config import config
from src.models.trasactions import Transaction
from src.models.users import User

class DbConfig:
    @classmethod
    async def init_db(cls):
        client = AsyncIOMotorClient(config.DB_URI)
        print("db connected")
        await init_beanie( database= client.get_database("fido"), document_models=[
            User,
            Transaction
        ])
