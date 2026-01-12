from django.db import models
from projects.models import Project
# from django.contrib.auth.models import User
from django.conf import settings

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
    rules = models.ManyToManyField('automation.AutomationRule', through='TaskRuleAssignment')

    def __str__(self):
        return self.name
    

class Milestone(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='milestones')
    name = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)

class Comments(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    Comment = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Resources(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='resources')
    resource = models.TextField()

class TaskRuleAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    rule = models.ForeignKey('automation.AutomationRule', on_delete=models.CASCADE)