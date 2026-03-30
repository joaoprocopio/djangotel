import unicodedata

from rastro_base.value_object import ValueObject


class Email(ValueObject[str]):
    def normalize(self) -> str:
        return self.value.strip().lower()


class Username(ValueObject[str]):
    def normalize(self) -> str:
        return unicodedata.normalize("NFKC", self.value)


class RawPassword(ValueObject[str]): ...


class HashedPassword(ValueObject[str]): ...
