from django.db import models

from rastro.tasks.domain.value_objects import TaskPriority, TaskStatus


class TaskModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        choices=[(status.value, status.value.title()) for status in TaskStatus],
        default=TaskStatus.OPEN,
    )
    priority = models.CharField(
        choices=[(priority.value, priority.value.title()) for priority in TaskPriority],
        default=TaskPriority.MEDIUM,
    )
    due_date = models.DateTimeField(null=True, blank=True)
    owner_id = models.IntegerField()
    assignee_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
