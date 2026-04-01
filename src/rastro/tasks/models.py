from django.db import models

from rastro.tasks.domain.value_objects import TaskPriority, TaskStatus
from rastro_shared_kernel.utils import str_enum_to_choices


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        choices=str_enum_to_choices(TaskStatus),
        default=TaskStatus.OPEN,
    )
    priority = models.CharField(
        choices=str_enum_to_choices(TaskPriority),
        default=TaskPriority.MEDIUM,
    )
    due_date = models.DateTimeField(null=True, blank=True)
    owner_id = models.IntegerField()
    assignee_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
