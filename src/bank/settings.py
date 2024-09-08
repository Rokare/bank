from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import MariaDBDsn, MySQLDsn, PostgresDsn, SecretStr
from functools import lru_cache


class Settings(BaseSettings):
    database_uri: PostgresDsn | MySQLDsn | MariaDBDsn
    database_type: str
    host: str
    database_user: str
    database_secret: str
    database_port: int
    database_schema: str

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local", ".env.prod"), extra="ignore"
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
