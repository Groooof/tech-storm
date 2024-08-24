from datetime import timedelta
from enum import Enum
from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class ServerRole(str, Enum):
    local = "local"
    dev = "dev"
    prod = "prod"


class Settings(BaseSettings):
    database_url: PostgresDsn = PostgresDsn("postgres://admin:admin@localhost:5555/techstorm")
    secret_key: str = "qwerty1234567890"
    users_access_token_lifetime: timedelta = timedelta(hours=10)
    users_access_token_lifetime: timedelta = timedelta(minutes=60)
    users_refresh_token_lifetime: timedelta = timedelta(days=30)
    server_role: ServerRole = ServerRole.local
    scenarios_claims_google_chat_url: str = (
        'https://chat.googleapis.com/v1/spaces/AAAAL5qjBKk/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=327TKkmXmLMVh1he_DFs4M6eGDTwIFCNbl-_nowl5uM'
    )

    @property
    def is_prod(self):
        return self.server_role == ServerRole.prod

    @property
    def is_local(self):
        return self.server_role == ServerRole.local

    @property
    def is_dev(self):
        return self.server_role == ServerRole.dev


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
