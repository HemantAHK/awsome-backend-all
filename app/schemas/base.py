from pydantic import (
    UUID4,
    BaseModel,
    ConfigDict,
    Field,
    SkipValidation,
    field_serializer,
)


class RWSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        validation=False,
    )

    uuid: UUID4 = Field(
        ..., examples=["ad3aa3d0-c35d-4eb0-bfd5-40a91774951c"]
    )

    @field_serializer("uuid", when_used="json")
    def serialize_uuid(self, uuid: UUID4) -> str:
        return str(uuid)
