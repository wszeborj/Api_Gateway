from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "API Gateway"
    DEBUG: bool = False
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    AUTH0_CLIENT_ID: str
    AUTH0_CLIENT_SECRET: str
    AUTH0_DOMAIN: str
    APP_SECRET_KEY: str
    AUTH0_API_AUDIENCE: str
    AUTH0_ALGORITHMS: str

    # Microservices URLs
    COURSE_SERVICE_URL: str = "http://course_service:8000/api/v1/"

    # Timeouts
    SERVICE_TIMEOUT: int = 30

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def AUTH0_ISSUER(self) -> str:
        return (
            f"https://{self.AUTH0_DOMAIN}/"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings: Settings = get_settings()