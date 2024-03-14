import logging

from pydantic import SecretStr

from app.core.settings.app import Settings


class TestAppSettings(Settings):
    DEBUG: bool = True

    APP_NAME: str = "Test FastAPI example application"

    SECRET_KEY: SecretStr = SecretStr("test_secret")

    LOGGING_LEVEL: int = logging.DEBUG
