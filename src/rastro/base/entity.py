from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar, cast

from rastro.base.error import InvalidIdError
from rastro.base.value_object import ValueObject

ID = TypeVar("ID")


@dataclass
class Entity(ABC, Generic[ID]):
    id: ID

    def __eq__(self, other: object) -> bool:
        if type(other) is not type(self):
            return NotImplemented

        other_entity: Entity[ID] = cast(Entity[ID], other)
        return self.id == other_entity.id

    def __hash__(self) -> int:
        return hash(self.id)


class Id(ValueObject[int]):
    def validate(self) -> None:
        if self.value < 1:
            raise InvalidIdError()
