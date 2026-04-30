from typing import Generic, TypeVar

from pydantic import BaseModel

ID = TypeVar("ID")


class Entity(BaseModel, Generic[ID]):
    id: ID

    def __eq__(self, other: object) -> bool:
        if type(other) is not type(self):
            return NotImplemented
        return bool(self.id == other.id)

    def __hash__(self) -> int:
        return hash(self.id)
