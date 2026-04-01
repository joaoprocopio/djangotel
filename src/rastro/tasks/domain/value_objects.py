from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Self

from rastro.tasks.domain.errors import (
    InvalidTaskDescriptionError,
    InvalidTaskTitleError,
)
from rastro_base.value_object import ValueObject
from rastro_shared_kernel.mixins import Validate


@dataclass(frozen=True)
class TaskTitle(ValueObject, Validate):
    value: str

    def validate(self) -> Self:
        if len(self.value) < 1 or len(self.value) > 200:
            raise InvalidTaskTitleError()
        return self


@dataclass(frozen=True)
class TaskDescription(ValueObject, Validate):
    value: str

    def validate(self) -> Self:
        if len(self.value) > 2000:
            raise InvalidTaskDescriptionError()
        return self


class TaskStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    DONE = "done"
    CLOSED = "closed"


class TaskPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class TaskDueDate(ValueObject):
    value: datetime
