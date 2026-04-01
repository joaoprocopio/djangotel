from dataclasses import dataclass
from typing import Optional

from rastro.tasks.domain.value_objects import (
    TaskDescription,
    TaskDueDate,
    TaskPriority,
    TaskStatus,
    TaskTitle,
)
from rastro_base.entity import Entity
from rastro_shared_kernel.value_objects import Id


@dataclass
class Task(Entity[Id]):
    title: TaskTitle
    description: TaskDescription
    status: TaskStatus
    priority: TaskPriority
    due_date: TaskDueDate
    owner_id: Id
    assignee_id: Optional[Id]
