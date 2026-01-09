from django.db import models
from projects.models import Project
from tasks.models import Task

class Trigger(models.Model):
    class SourceType(models.TextChoices):
        Task="TASK", "Task"
        TIME="TIME", "Time"
        SYSTEM="SYSTEM", "System"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="triggers")
    source_type = models.CharField(max_length=20, choices=SourceType.choices)
    condition = models.JSONField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Trigger {self.id} ({self.source_type})"


class Action(models.Model):
    class ActionType(models.TextChoices):
        TYPE_EMAIL = "EMAIL"," Email"
        TYPE_WEBHOOK = "WEBHOOK", "Webhook"
        TYPE_NOTIFICATION = "NOTIFICATION","notification"

    trigger = models.ForeignKey(Trigger, on_delete=models.CASCADE, related_name="actions")
    type = models.CharField(max_length=30, choices=ActionType.choices)
    config = models.JSONField()
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"Action {self.type} for Trigger {self.trigger_id}"


class JobExecution(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    action = models.ForeignKey(Action, on_delete=models.CASCADE, related_name="executions")
    related_task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    attempt_number = models.PositiveIntegerField(default=1)

    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"JobExecution {self.id} for Action {self.action_id} - Status: {self.status}"
    


class EventLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="events")
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    occurred_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.event_type