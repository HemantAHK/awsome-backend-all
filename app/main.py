from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.dependencies.limiter import limiter
from app.api.v1.api import router as api_router
from app.core.config import get_app_settings
from app.core.events import lifespan
from app.middleware.request import (
    STARLETTEProcessTimeMiddleware,
    STARLETTERequestIDMiddleware,
    log_request_middleware,
)


def get_application() -> FastAPI:
    settings = get_app_settings()

    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs, lifespan=lifespan)

    application.middleware("http")(log_request_middleware)
    application.add_middleware(STARLETTEProcessTimeMiddleware)
    application.add_middleware(STARLETTERequestIDMiddleware)
    application.add_middleware(GZipMiddleware, minimum_size=1000)

    application.include_router(api_router, prefix=settings.API_PREFIX)

    application.state.limiter = limiter

    application.add_exception_handler(
        RateLimitExceeded, _rate_limit_exceeded_handler
    )

    return application


app = get_application()
