from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from rastro_base.dto import DTO
from rastro_shared_kernel.mixins import FromJson


@dataclass(frozen=True)
class CreateTaskInput(DTO, FromJson):
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[datetime]
    assignee_id: Optional[int]


@dataclass(frozen=True)
class UpdateTaskInput(DTO, FromJson):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]
    priority: Optional[str]
    due_date: Optional[datetime]
    assignee_id: Optional[int]


@dataclass(frozen=True)
class TaskOutput(DTO):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[datetime]
    owner_id: int
    assignee_id: Optional[int]
