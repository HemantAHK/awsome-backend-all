from typing import List

from pydantic import BaseModel, Field

from app.schemas.base import RWSchema


class Sample(BaseModel):
    name: str = Field(examples=["Example name"])
    task: str = Field(examples=["Example task"])


class SampleInDB(Sample, RWSchema):
    is_active: bool


class SampleInCreate(Sample):
    ...


class SampleInUpdate(Sample):
    ...


class SampleInResponse(Sample, RWSchema):
    ...
