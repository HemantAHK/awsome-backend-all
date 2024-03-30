import os
from typing import cast

from sqlalchemy import Boolean, Column, String, text

from app.core.config import get_app_settings
from app.db.session import BaseDBModel
from app.models.base import (
    ActiveStatusMixin,
    CreatedMixin,
    CreatedModifiedMixin,
    IdMixin,
    UuidMixin,
)

settings = get_app_settings()


class DBUser(
    IdMixin,
    UuidMixin,
    CreatedModifiedMixin,
    CreatedMixin,
    ActiveStatusMixin,
    BaseDBModel,
):

    __tablename__ = "users"
    __table_args__ = {"schema": settings.POSTGRES_SCHEMA}

    first_name = cast(str, Column(String(256), nullable=True))
    last_name = cast(str, Column(String(256), nullable=True))

    email = cast(
        str, Column(String, index=True, nullable=False, unique=True)
    )
    password = cast(str, Column(String, nullable=False))
    verification_code = cast(str, Column(String, nullable=True))
    is_verified = cast(
        bool,
        Column(Boolean, default=False, server_default=text("false")),
    )
