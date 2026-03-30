import re
import unicodedata

from rastro.auth.domain.errors import (
    InvalidEmailError,
    InvalidPasswordError,
    InvalidUsernameError,
)
from rastro_base.value_object import ValueObject


class Email(ValueObject[str]):
    # https://emailregex.com/
    EMAIL_PATTERN = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    def normalize(self) -> str:
        return self.value.strip().lower()

    def validate(self) -> None:
        if not self.EMAIL_PATTERN.match(self.value):
            raise InvalidEmailError()


class Username(ValueObject[str]):
    UNICODE_USERNAME_PATTERN = re.compile(r"^[\w.@+-]+\Z")

    def normalize(self) -> str:
        return unicodedata.normalize("NFKC", self.value)

    def validate(self) -> None:
        if not self.UNICODE_USERNAME_PATTERN.match(self.value):
            raise InvalidUsernameError()


class RawPassword(ValueObject[str]):
    def validate(self) -> None:
        if len(self.value) < 8:
            raise InvalidPasswordError()


class HashedPassword(ValueObject[str]): ...
