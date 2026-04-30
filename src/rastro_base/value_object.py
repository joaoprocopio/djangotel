from typing import TypeVar

from pydantic import BaseModel, ConfigDict, RootModel


class ValueObject(BaseModel):
    model_config = ConfigDict(frozen=True)

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.model_dump().items())))

    def __eq__(self, other: object) -> bool:
        if type(other) is not type(self):
            return NotImplemented
        return hash(self) == hash(self.model_dump)


T = TypeVar("T")


class RootValueObject(RootModel[T]):
    model_config = ConfigDict(frozen=True)

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.model_dump().items())))

    def __eq__(self, other: object) -> bool:
        if type(other) is not type(self):
            return NotImplemented
        return hash(self) == hash(self.model_dump)
