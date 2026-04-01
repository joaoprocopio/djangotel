from abc import ABC
from typing import TypeVar

T = TypeVar("T")


class ValueObject(ABC):
    def setattr(self, attr: str, value: T) -> None:
        object.__setattr__(self, attr, value)
