from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeVar
from uuid import uuid4

T = TypeVar("T")


@dataclass(frozen=True)
class DomainEvent(ABC):
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    event_type: str = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "event_type", self.__class__.__name__)
