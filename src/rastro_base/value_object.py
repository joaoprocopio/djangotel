from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class ValueObject(ABC, Generic[T]):
    value: T

    def normalize(self) -> T:
        return self.value

    def validate(self) -> None: ...

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", self.normalize())
        self.validate()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.value!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
