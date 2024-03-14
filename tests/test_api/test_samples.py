
import unittest

import pytest
from fastapi import FastAPI, HTTPException
from app.schemas.sample import SampleInResponse, SampleInCreate
from app.repositories.sample import SamplesRepository
from httpx import AsyncClient
from starlette.status import HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY
from fastapi.exceptions import ResponseValidationError
from typing import List, Tuple, Dict, Any, Type, Union

from unittest.mock import MagicMock
from loguru import logger


# # This is a global variable that will store the test cases from the happy path tests
happy_path_tests = []


# # This is a fixture that will yield the test cases from the happy path tests
# @pytest.fixture(params=happy_path_tests)
# def happy_test_case(request):
#     return request.param


@pytest.mark.anyio
@pytest.mark.parametrize(
    "test_id,payload,status_code,response_model",
    [
        # Happy path tests with various realistic test values
        ("happy-1", {"name": "Sample A", "task": "Task A"},
         HTTP_200_OK, SampleInResponse),
        ("happy-2", {"name": "Sample B", "task": "Task B"},
         HTTP_200_OK, SampleInResponse),
        # # Edge cases
        # ("edge-1", {"name": "", "task": ""}, HTTP_422_UNPROCESSABLE_ENTITY,
        #  HTTPException),  # Empty name and task
        # # Error cases
        # ("error-1", {"name": "Sample C", "task": "Task C"},
        #  HTTP_400_BAD_REQUEST, HTTPException),  # Error case
    ],

)
async def test_create_sample(
    test_id: str,
    payload: dict,
    status_code: int,
    response_model: type,
    async_client: AsyncClient,
    app: FastAPI,
):
    logger.info(f"Test ID: {test_id}")

    # Arrange
    sample_in_create = SampleInCreate(**payload)

    # Act
    try:
        response = await async_client.post(app.url_path_for("sample:create"), json=payload)
    except ResponseValidationError as e:
        logger.error(f"Response validation error: {e}")
        logger.error(f"Validation errors: {e.errors()}")
        raise

    # Assert
    assert response.status_code == status_code
    if response_model is SampleInResponse:
        response_json = response.json()
        assert response_json["name"] == sample_in_create.name
        assert response_json["task"] == sample_in_create.task
        assert "uuid" in response_json

        # If the test is a happy path test, store the entire test case for later use
        if test_id.startswith("happy"):
            happy_path_tests.append(
                (test_id, payload, status_code, response_model, response_json["uuid"]))

    elif response_model is HTTPException:
        assert response.json().get('detail') is not None


# @pytest.mark.anyio
# async def test_get_sample(happy_test_case: Tuple, async_client: AsyncClient, app: FastAPI):

#     # Unpack the test case
#     test_id, payload, status_code, response_model, uuid = happy_test_case

#     # Use the UUIDs from the happy path tests to get the samples
#     response = await async_client.get(app.url_path_for("sample:get_one", sample_id=uuid))
#     assert response.status_code == status_code
