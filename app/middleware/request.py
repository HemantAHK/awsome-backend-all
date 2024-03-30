import http
import time
import uuid

from fastapi import Request
from loguru import logger
from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send


async def log_request_middleware(request: Request, call_next):
    """
    This middleware will log all requests and their processing time.

    E.g. log:
    0.0.0.0:1234 - GET /ping 200 OK 1.00ms
    """
    logger.debug("middleware: log_request_middleware")

    # Extracting relevant information from the request
    url = (
        f"{request.url.path}?{request.query_params}"
        if request.query_params
        else request.url.path
    )
    method = request.method
    client_host = getattr(
        getattr(request, "client", None), "host", None
    )
    client_port = getattr(
        getattr(request, "client", None), "port", None
    )

    # Measuring the processing time
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)

    # Extracting response information
    status_code = response.status_code
    try:
        status_phrase = http.HTTPStatus(status_code).phrase
    except ValueError:
        status_phrase = ""

    # Logging the information
    log_message = (
        f'{client_host}:{client_port} - "{method} {url}" '
        f"{status_code} {status_phrase} {formatted_process_time}ms"
    )
    logger.info(log_message)

    return response


class STARLETTEProcessTimeMiddleware:
    app: ASGIApp

    def __init__(
        self,
        app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        start_time = time.time()

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append(
                    "X-Process-Time", str(time.time() - start_time)
                )
            await send(message)

        await self.app(scope, receive, send_wrapper)


class STARLETTERequestIDMiddleware:
    """
    Load request ID from headers if present.

    Generate one otherwise.
    """

    app: ASGIApp

    def __init__(
        self,
        app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = str(uuid.uuid4())
        with logger.contextualize(request_id=request_id):
            # Log before request processing
            logger.info("[STARTED] ")

            async def send_wrapper(message: Message) -> None:
                if message["type"] == "http.response.start":
                    headers = MutableHeaders(scope=message)
                    headers.append("X-Request-ID", request_id)
                await send(message)

            try:
                await self.app(scope, receive, send_wrapper)
            finally:
                # Log after request processing
                logger.info("[ENDED]")
