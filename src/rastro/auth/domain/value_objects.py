import unicodedata

from rastro.auth.domain.errors import InvalidPasswordError
from rastro_base.value_object import ValueObject


class Email(ValueObject[str]):
    def normalize(self) -> str:
        return self.value.strip().lower()


class Username(ValueObject[str]):
    def normalize(self) -> str:
        return unicodedata.normalize("NFKC", self.value)


class RawPassword(ValueObject[str]):
    def validate(self) -> None:
        if len(self.value) < 8:
            raise InvalidPasswordError()


class HashedPassword(ValueObject[str]): ...
