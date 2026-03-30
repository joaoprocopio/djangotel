import json
from dataclasses import dataclass, fields
from typing import Self

from rastro.base.dto import DTO
from rastro.base.mixins import FromStr


@dataclass(frozen=True)
class SignUpInput(DTO, FromStr):
    username: str
    email: str
    password: str

    @classmethod
    def from_str(cls, bytes: str | bytes | bytearray) -> Self:
        data = json.loads(value)
        return cls(**{field.name: data[field.name] for field in fields(cls)})


@dataclass(frozen=True)
class SignInInput(DTO):
    query: str
    password: str


@dataclass(frozen=True)
class UserOutput(DTO):
    id: int
    email: str
    username: str
    is_active: bool
    is_verified: bool


@dataclass(frozen=True)
class RequestPasswordResetInput(DTO):
    email: str


@dataclass(frozen=True)
class ResetPasswordInput(DTO):
    user_id: int
    token: str
    new_password: str


@dataclass(frozen=True)
class RequestEmailVerificationInput(DTO):
    user_id: int


@dataclass(frozen=True)
class VerifyEmailInput(DTO):
    user_id: int
    token: str


@dataclass(frozen=True)
class GetUserInput(DTO):
    user_id: int
