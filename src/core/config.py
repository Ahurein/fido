from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    DB_URI: str
    VERSION: str = "v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

config = Config()