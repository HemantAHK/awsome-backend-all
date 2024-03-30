import datetime
import enum
import hashlib
import re
from typing import Any, Self

from pydantic import (
    UUID4,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    SecretStr,
    field_serializer,
    field_validator,
    model_serializer,
    model_validator,
)

VALID_PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
)
VALID_NAME_REGEX = re.compile(r"^[a-zA-Z]{2,}$")


class Role(enum.IntFlag):
    User = 0
    Author = 1
    Editor = 2
    Admin = 4
    SuperAdmin = 8


def convert_datetime_to_realworld(dt: datetime.datetime) -> str:
    return (
        dt.replace(tzinfo=datetime.timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(string.split("_"))
    )


class User(BaseModel):
    name: str = Field(examples=["Example"])

    email: EmailStr = Field(
        examples=["user@arjancodes.com"],
        description="The email address of the user",
        frozen=True,
    )

    password: SecretStr = Field(
        examples=["Password123"],
        description="The password of the user",
        exclude=True,
    )
    role: Role = Field(
        description="The role of the user",
        examples=[1, 2, 4, 8],
        default=0,
        validate_default=True,
    )

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        if not VALID_NAME_REGEX.match(v):
            raise ValueError(
                "Name is invalid, must contain only letters and be at least 2 characters long"
            )
        return v

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, v: int | str | Role) -> Role:
        op = {
            int: lambda x: Role(x),
            str: lambda x: Role[x],
            Role: lambda x: x,
        }
        try:
            return op[type(v)](v)
        except (KeyError, ValueError) as e:
            raise ValueError(
                f'Role is invalid, please use one of the following: {", ".join([x.name for x in Role])}'
            ) from e

    @model_validator(mode="before")
    @classmethod
    def validate_user_pre(cls, v: dict[str, Any]) -> dict[str, Any]:
        if "name" not in v or "password" not in v:
            raise ValueError("Name and password are required")
        if v["name"].casefold() in v["password"].casefold():
            raise ValueError("Password cannot contain name")
        if not VALID_PASSWORD_REGEX.match(v["password"]):
            raise ValueError(
                "Password is invalid, must contain 8 characters, 1 uppercase, 1 lowercase, 1 number"
            )
        v["password"] = hashlib.sha256(
            v["password"].encode()
        ).hexdigest()
        return v

    @model_validator(mode="after")
    def validate_user_post(self, v: Any) -> Self:
        if self.role == Role.Admin and self.name != "Hemant":
            raise ValueError("Only Hemant can be an admin")
        return self

    @field_serializer("role", when_used="json")
    @classmethod
    def serialize_role(cls, v) -> str:
        return v.name

    @model_serializer(mode="wrap", when_used="json")
    def serialize_user(self, serializer, info) -> dict[str, Any]:
        if not info.include and not info.exclude:
            return {"name": self.name, "role": self.role.name}
        return serializer(self)

    @field_serializer("uuid", when_used="json")
    def serialize_id(self, uuid: UUID4) -> str:
        return str(uuid)

    @model_validator(mode="before")
    @classmethod
    def set_null_microseconds(
        cls, data: dict[str, Any]
    ) -> dict[str, Any]:
        datetime_fields = {
            k: v.replace(microsecond=0)
            for k, v in data.items()
            if isinstance(k, datetime)
        }

    # TODO[pydantic]: The following keys were removed: `json_encoders`.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-config for more information.
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_encoders={
            datetime.datetime: convert_datetime_to_realworld
        },
        alias_generator=convert_field_to_camel_case,
    )
