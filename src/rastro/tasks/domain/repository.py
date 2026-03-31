from abc import ABC, abstractmethod
from typing import Optional

from rastro.tasks.domain.entities import Task
from rastro.tasks.domain.value_objects import (
    TaskDescription,
    TaskDueDate,
    TaskPriority,
    TaskStatus,
    TaskTitle,
)
from rastro_base.entity import Id


class TaskRepository(ABC):
    @abstractmethod
    def create(
        self,
        title: TaskTitle,
        description: TaskDescription,
        status: TaskStatus,
        priority: TaskPriority,
        due_date: TaskDueDate,
        owner_id: Id,
        assignee_id: Optional[Id],
    ) -> Task: ...

    @abstractmethod
    def get_by_id(self, id: Id) -> Optional[Task]: ...

    @abstractmethod
    def list_by_owner(self, owner_id: Id) -> list[Task]: ...

    @abstractmethod
    def list_by_assignee(self, assignee_id: Id) -> list[Task]: ...

    @abstractmethod
    def update(
        self,
        id: Id,
        title: Optional[TaskTitle] = None,
        description: Optional[TaskDescription] = None,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        due_date: Optional[TaskDueDate] = None,
        assignee_id: Optional[Id] = None,
    ) -> Task: ...

    @abstractmethod
    def delete(self, id: Id) -> None: ...
