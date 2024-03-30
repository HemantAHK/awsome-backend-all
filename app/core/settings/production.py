from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.settings.app import Settings


class ProdAppSettings(Settings):

    model_config = SettingsConfigDict(env_file="prod.env")
