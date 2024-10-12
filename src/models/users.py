from beanie import Indexed, Document

from src.models.base_model import DocumentBaseModel


class User(Document):
    first_name: str
    last_name: str

    class Settings:
        name = "fido_users"