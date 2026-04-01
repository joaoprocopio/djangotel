from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar, cast

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
