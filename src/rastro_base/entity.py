from typing import Generic, TypeVar

from rastro_base.pydantic import BaseModel

ID = TypeVar("ID")


class Entity(BaseModel, Generic[ID]):
    id: ID
