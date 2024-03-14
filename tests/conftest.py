from os import environ
from typing import Generator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from asyncpg.pool import Pool
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient

from tests.fake_asyncpg_pool import FakeAsyncPGPool

environ["APP_ENV"] = "dev"


@pytest.fixture(scope="module")
def app() -> FastAPI:
    from app.main import (
        get_application,  # local import for testing purpose
    )

    return get_application()


@pytest.fixture(scope="module")
async def initialized_app(app: FastAPI) -> FastAPI:  # type: ignore
    async with LifespanManager(app):
        app.state.pool = await FakeAsyncPGPool.create_pool(
            app.state.pool
        )
        yield app


@pytest.fixture(scope="module")
def pool(initialized_app: FastAPI) -> Pool:

    return initialized_app.state.pool


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def async_client(initialized_app: FastAPI) -> AsyncClient:  # type: ignore
    async with AsyncClient(
        app=initialized_app,
        base_url="http://testserver:8000",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client
