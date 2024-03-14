import asyncpg
from fastapi import FastAPI
from loguru import logger

from app.core.config import get_app_settings
from app.core.settings.app import Settings


async def connect_to_db(
    app: FastAPI,
) -> None:

    settings: Settings = get_app_settings()

    logger.info("Connecting to PostgreSQL")

    logger.info(
        f"{settings.POSTGRES_SYNC_PREFIX}{settings.POSTGRES_URI}"
    )

    app.state.pool = await asyncpg.create_pool(
        f"{settings.POSTGRES_SYNC_PREFIX}{settings.POSTGRES_URI}",
        min_size=settings.MIN_CONNECTION_COUNT,
        max_size=settings.MAX_CONNECTION_COUNT,
    )

    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app.state.pool.close()

    logger.info("Connection closed")
