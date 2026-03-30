import re

from rastro.base.parser import is_valid_email
from rastro.base.value_object import ValueObject
from rastro.users.domain.errors import (
    InvalidEmailError,
    InvalidPasswordError,
    InvalidUsernameError,
)


class Email(ValueObject[str]):
    def validate(self) -> None:
        if not self.value:
            raise InvalidEmailError("Email cannot be empty")
        if not is_valid_email(self.value):
            raise InvalidEmailError(f"Invalid email format: {self.value}")


class Username(ValueObject[str]):
    USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]+$")

    def validate(self) -> None:
        if not self.value:
            raise InvalidUsernameError("Username cannot be empty")
        if len(self.value) > 50:
            raise InvalidUsernameError("Username cannot exceed 50 characters")
        if not self.USERNAME_PATTERN.match(self.value):
            raise InvalidUsernameError(
                "Username can only contain alphanumeric characters and underscores"
            )


class RawPassword(ValueObject[str]):
    MIN_LENGTH = 8

    def validate(self) -> None:
        if not self.value:
            raise InvalidPasswordError("Password cannot be empty")
        if len(self.value) < self.MIN_LENGTH:
            raise InvalidPasswordError(
                f"Password must be at least {self.MIN_LENGTH} characters"
            )


class HashedPassword(ValueObject[str]):
    def validate(self) -> None:
        if not self.value:
            raise InvalidPasswordError("Hashed password cannot be empty")
