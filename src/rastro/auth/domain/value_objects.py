import re
import unicodedata
from dataclasses import dataclass
from typing import Self

from rastro.auth.domain.errors import (
    InvalidEmailError,
    InvalidPasswordError,
    InvalidUsernameError,
)
from rastro_base.value_object import ValueObject
from rastro_shared_kernel.mixins import Normalize, Validate

# https://emailregex.com/
EMAIL_PATTERN = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
UNICODE_USERNAME_PATTERN = re.compile(r"^[\w.@+-]+\Z")


@dataclass(frozen=True)
class Email(ValueObject, Normalize, Validate):
    value: str

    def normalize(self) -> Self:
        self.setattr("value", self.value.strip().lower())
        return self

    def validate(self) -> Self:
        if not EMAIL_PATTERN.match(self.value):
            raise InvalidEmailError()
        return self


@dataclass(frozen=True)
class Username(ValueObject, Normalize, Validate):
    value: str

    def normalize(self) -> Self:
        self.setattr("value", unicodedata.normalize("NFKC", self.value))
        return self

    def validate(self) -> Self:
        if not UNICODE_USERNAME_PATTERN.match(self.value):
            raise InvalidUsernameError()
        return self


@dataclass(frozen=True)
class RawPassword(ValueObject, Validate):
    value: str

    def validate(self) -> Self:
        if len(self.value) < 8:
            raise InvalidPasswordError()
        return self


@dataclass(frozen=True)
class HashedPassword(ValueObject):
    value: str
