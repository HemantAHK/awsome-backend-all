from contextlib import asynccontextmanager
from typing import Callable

from fastapi import Depends, FastAPI
from loguru import logger

from app.core.settings.app import AppSettings, Settings
from app.db.events import close_db_connection, connect_to_db


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    try:
        # Startup logic
        await connect_to_db(app)
        yield
    finally:
        # Shutdown logic
        await close_db_connection(app)
