from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DB_URI: str
    FERNET_KEY: str
    VERSION: str = "v1"
    REDIS_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


config = Config()
