from abc import ABC
from typing import Protocol

from rastro.base.entities import Entity
from rastro.base.aggregates import AggregateRoot


class DomainService(ABC):
    pass


class Repository(Protocol):
    def add(self, entity: Entity[object]) -> Entity[object]: ...
    def get(self, id: object) -> Entity[object] | None: ...
    def remove(self, entity: Entity[object]) -> None: ...


class UnitOfWork(Protocol):
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
