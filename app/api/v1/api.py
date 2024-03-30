from fastapi import APIRouter

from app.api.v1.endpoints import authentication, sample, tenants, users

router = APIRouter()


router.include_router(
    authentication.router, tags=["authentication"], prefix="/auth"
)

# router.include_router(
#     sample.router, tags=["samples"], prefix="/samples"
# )

router.include_router(
    tenants.router, tags=["tenants"], prefix="/tenants"
)

router.include_router(users.router, tags=["users"], prefix="/users")
