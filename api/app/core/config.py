import secrets
from functools import lru_cache
from typing import List

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    DEBUG: bool = False

    PROJECT_NAME: str = "got"
    API_V1_STR: str = "/api/v1"
    API_APP: str = "app.main:app"
    # SERVER_HOSTNAME: str
    BASE_URL: str
    PORT: int = 9000

    REDIS_HOST: str
    REDIS_PORT: int

    # CORS_ORIGINS is a str comma separated origins
    # e.g: "http://localhost,http://localhost:9000,http://localhost:8008"
    CORS_ORIGINS: str = ""

    @validator("CORS_ORIGINS")
    def assemble_cors_origins(cls, v: str) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        raise ValueError(v)

    SECRET_KEY: str = secrets.token_urlsafe(32)

    DATABASE_URL: str

    OMDB_API_KEY: str

    class Config:
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()
