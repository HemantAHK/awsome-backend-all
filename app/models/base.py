import uuid
from datetime import datetime
from typing import Optional, cast

from pydantic.types import UUID4
from pytz import timezone
from sqlalchemy import Boolean, Column, DateTime, Integer, text
from sqlalchemy.dialects.postgresql import UUID


class ActiveStatusMixin:
    is_active = cast(
        bool, Column(Boolean, default=True, server_default="true")
    )
    deactivated_at = cast(bool, Column(DateTime))


class CreatedMixin:
    created_by = cast(Optional[int], Column(Integer, index=True))
    created_at = cast(
        datetime,
        Column(
            DateTime,
            default=datetime.now(tz=timezone("UTC")),
        ),
    )


class CreatedModifiedMixin:
    updated_by = cast(Optional[int], Column(Integer, index=True))
    updated_at = cast(
        datetime,
        Column(
            DateTime,
            default=datetime.now(tz=timezone("UTC")),
            onupdate=datetime.now(tz=timezone("UTC")),
        ),
    )


class IdMixin:
    id = cast(
        int,
        Column(
            Integer,
            primary_key=True,
            index=True,
            autoincrement=True,
            unique=True,
        ),
    )


class UuidMixin:
    uuid = cast(
        UUID4,
        Column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            index=True,
            server_default=text("gen_random_uuid()"),
            unique=True,
        ),
    )
