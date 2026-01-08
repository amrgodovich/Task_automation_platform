from django.db import models
from projects.models import Project

# Create your models here.
class Task(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        RUNNING = "RUNNING", "Running"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"
        CANCELLED = "CANCELLED", "Cancelled"
    task_id=models.AutoField(primary_key=True)
    project=models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks')
    name= models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=50,choices=Status.choices,default=Status.PENDING)

    def __str__(self):
        return self.name