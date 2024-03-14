import sys
from typing import Union

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from loguru import logger
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


async def request_validation_exception_handler(
    request: Request,
    exc: Union[RequestValidationError, ValidationError],
) -> JSONResponse:
    """
    This is a wrapper to the default RequestValidationException handler of FastAPI.

    This function will be called when client input is not valid.
    """

    try:

        log_message = (
            f"Request Validation Error occurred: {exc.errors()}"
        )
        logger.error(
            log_message,
        )

        return JSONResponse(
            {"errors": exc._errors[0]["msg"]},
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except Exception as ex:
        logger.error(f"Unhandled exception occurred. | details: {ex}")


async def http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    """
    This is a wrapper to the default HTTPException handler of FastAPI.

    This function will be called when a HTTPException is explicitly raised.
    """
    error_detail = {
        "error": {
            "code": exc.status_code,
            "message": exc.detail,
            "headers": dict(request.headers),
            "path": request.url.path,
            # You can add more details as needed
        }
    }

    log_message = (
        f"HTTPException {exc.status_code} occurred: {exc.detail}"
    )
    logger.error(
        log_message,
        extra={"error_detail": error_detail, "path": request.url.path},
    )
    return JSONResponse(
        {"error": exc.detail}, status_code=exc.status_code
    )


async def unhandled_exception_handler(
    request: Request, exc: Exception
) -> PlainTextResponse:
    """
    This middleware will log all unhandled exceptions.

    Unhandled exceptions are all exceptions that are not HTTPExceptions or
    RequestValidationErrors.
    """

    (
        exception_type,
        exception_value,
        exception_traceback,
    ) = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)

    error_detail = {
        "error": {
            "type": exception_name,
            "message": str(exception_value),
            "traceback": str(exception_traceback),
            "path": request.url.path,
            # You can add more details as needed
        }
    }

    log_message = f"Unhandled Exception occurred: {exception_name}: {exception_value}"
    logger.error(
        log_message,
        extra={"error_detail": error_detail, "path": request.url.path},
    )

    return PlainTextResponse(
        str(exc), status_code=HTTP_500_INTERNAL_SERVER_ERROR
    )
