import logging
import sys
from typing import Any, Dict, List, Optional, Tuple, Union

from loguru import logger
from pydantic import AnyHttpUrl, ConfigDict, SecretStr, field_validator

from app.core.logging import InterceptHandler
from app.core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    APP_NAME: str = "FastAPI app"
    APP_DESCRIPTION: str | None = None
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    DOCS_URL: str = "/docs"
    API_PREFIX: str = "/api"
    OPENAPI_PREFIX: str = ""
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    LICENSE_NAME: str | None = None
    CONTACT_NAME: str | None = None
    CONTACT_EMAIL: str | None = None


class APISettings(BaseAppSettings):
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl | str] = ["*"]
    BACKEND_CORS_ORIGIN_REGEX: Optional[
        str
    ] = r"^https:\/\/.*\.(netlify\.app|herokuapp\.com)\/?$"  # noqa: W605

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(
        cls, v: Union[str, List[str]]
    ) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            print(v)
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


class PostgresSettings(BaseAppSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "Password"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "ems"
    POSTGRES_SYNC_PREFIX: str = "postgresql://"
    POSTGRES_ASYNC_PREFIX: str = "postgresql+asyncpg://"
    POSTGRES_URI: str = f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    POSTGRES_URL: str | None = None
    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = -1
    POOL_PRE_PING: bool = True
    ECHO: bool = False
    POOL_RECYCLE_IN_SECONDS: int = 3600
    ECHO_POOL: bool = False
    POOL_RESET_ON_RETURN: str = "rollback"
    POOL_TIMEOUT_IN_SECONDS: int = 30
    POOL: str = "~sqlalchemy.pool.QueuePool"
    MAX_CONNECTION_COUNT: int = 10
    MIN_CONNECTION_COUNT: int = 10
    POSTGRES_SCHEMA: str = "dev"


class CryptSettings(BaseAppSettings):
    JWT_TOKEN_PREFIX: str = "Token"
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    SECRET_KEY: SecretStr = SecretStr("secret")


class FirstUserSettings(BaseAppSettings):
    ADMIN_NAME: str = "Admin"
    ADMIN_EMAIL: str = "admin@admin.com"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "Str1ng$t"


class TestSettings(BaseAppSettings):
    TEST_NAME: str = "Tester User"
    TEST_EMAIL: str = "test@tester.com"
    TEST_USERNAME: str = "testeruser"
    TEST_PASSWORD: str = "Str1ng$t"


class DefaultRateLimitSettings(BaseAppSettings):
    DEFAULT_RATE_LIMIT_LIMIT: int = 10
    DEFAULT_RATE_LIMIT_PERIOD: int = 3600


class LoggingSettings(BaseAppSettings):
    LOGGING_LEVEL: int = logging.INFO


class ClientSideCacheSettings(BaseAppSettings):
    CLIENT_CACHE_MAX_AGE: int = 60


class Settings(
    AppSettings,
    APISettings,
    PostgresSettings,
    CryptSettings,
    FirstUserSettings,
    TestSettings,
    DefaultRateLimitSettings,
    ClientSideCacheSettings,
    LoggingSettings,
):
    loggers: Tuple[str, ...] = (
        "uvicorn.asgi",
        "uvicorn.access",
        "gunicorn.error",
    )

    model_config = ConfigDict(validate_assignment=True)

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.DEBUG,
            "docs_url": self.DOCS_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "title": self.APP_NAME,
            "version": self.APP_VERSION,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [
                InterceptHandler(level=self.LOGGING_LEVEL)
            ]

        log_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <4}</level> | <yellow>{extra[request_id]: <4}</yellow> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"

        logger.configure(
            handlers=[
                {
                    "sink": sys.stderr,
                    "level": self.LOGGING_LEVEL,
                    "format": log_format,
                }
            ],
            extra={
                "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            },
        )
