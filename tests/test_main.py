import json

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from loguru import logger
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from app.main import get_application  # local import for testing purpose


class CollectionForTestCheck:
    def __init__(self):
        self.collected = []

    def pytest_collection_modifyitems(self, items):
        for item in items:
            self.collected.append(item.nodeid)


@pytest.mark.anyio
async def test_server_check(async_client: AsyncClient):
    response = await async_client.get("/docs")
    assert response.status_code == 200
    assert (
        response.headers["Content-Type"] == "text/html; charset=utf-8"
    )


@pytest.mark.anyio
async def test_openapi_json(async_client: AsyncClient):
    response = await async_client.get("/openapi.json")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    # Ensure that the response body is valid JSON
    try:
        json.loads(response.text)
    except json.JSONDecodeError:
        assert False, "Response body is not valid JSON"


# @pytest.mark.anyio
# async def test_check_all_endpoints_for_test_function(async_client: AsyncClient):
#     endpoints_response = await async_client.get("/openapi.json")
#     endpoint_paths = endpoints_response.json()['paths']
#     api_endpoint_functions = []
#     for endpoint in endpoint_paths:
#         for endpoint_method in endpoint_paths[endpoint]:
#             endpoint_slug = endpoint[1:].replace("/", "_")
#             length_of_suffix = len(f"_{endpoint_slug}_{endpoint_method}")
#             api_endpoint_functions.append(
#                 endpoint_paths[endpoint][endpoint_method]['operationId'][:-length_of_suffix])
#     coll = CollectionForTestCheck()
#     pytest.main(['--collect-only'], plugins=[coll])
#     test_functions = [
#         str(test_coll).split("::")[-1] for test_coll in coll.collected
#     ]
#     for api_endpoint_function in api_endpoint_functions:
#         assert (
#             f"test_{str(api_endpoint_function)}" in test_functions
#         ), f"Test function of {api_endpoint_function} couldn't found"
