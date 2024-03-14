import os
from sqlalchemy import Column, String

from app.db.session import BaseDBModel
from app.models.base import (
    ActiveStatusMixin,
    CreatedMixin,
    CreatedModifiedMixin,
    IdMixin,
    UuidMixin,
)
from app.core.config import get_app_settings


class DBSample(
    IdMixin,
    UuidMixin,
    CreatedModifiedMixin,
    CreatedMixin,
    ActiveStatusMixin,
    BaseDBModel,
):

    __tablename__ = "samples"

    name = Column(String)
    task = Column(String)
