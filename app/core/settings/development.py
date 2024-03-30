import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.settings.app import Settings


class DevAppSettings(Settings):
    DEBUG: bool = True

    APP_NAME: str = "EMS Backend (dev)"

    LOGGING_LEVEL: int = logging.DEBUG

    # model_config = SettingsConfigDict(env_file=".env")
