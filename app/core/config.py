import os
from typing import Literal

from pydantic import SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILES = {
    "dev": ".env",
    "test": ".env.test",
    "prod": ".env.prod",
}


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: SecretStr
    DB_NAME: str
    APP_PORT: int
    ADMINER_PORT: int
    ENV: Literal["dev", "test", "prod"]

    GRAFANA_ADMIN_USER: str
    GRAFANA_ADMIN_USER_PASSWORD: SecretStr

    @computed_field(repr=False)
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD.get_secret_value()}"
            f"@{self.DB_HOST}:5432/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(
        env_file=ENV_FILES.get(os.getenv("ENV", "dev"), ".env"),
        env_file_encoding="utf-8",
    )


settings = Settings()  # type: ignore
