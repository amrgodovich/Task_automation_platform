from django.db import models
from projects.models import Project, ProjectMember
# from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

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
    
from django.core.exceptions import ValidationError

class TaskMember(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(ProjectMember, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Check if the ProjectMember's project matches the Task's project
        if self.user.project_id != self.task.project_id:
            raise ValidationError("This user is not a member of the project this task belongs to.")

    def save(self, *args, **kwargs):
        self.full_clean() # Triggers the clean() method above
        super().save(*args, **kwargs)

    class Meta:
        # Prevent adding the same user to the same task twice
        unique_together = ('task', 'user')

    def __str__(self):
        return f"{self.user} - {self.task}"

@receiver(post_save, sender=Task)
def create_task_owner_membership(sender, instance, created, **kwargs):
    if created:
        # 1. Find the ProjectMember record for the project owner
        owner_member = ProjectMember.objects.filter(
            project=instance.project, 
            user=instance.project.owner
        ).first()

        # 2. Only create TaskMember if the owner is actually a ProjectMember
        if owner_member:
            TaskMember.objects.get_or_create(
                task=instance,
                user=owner_member
            )
class Milestone(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='milestones')
    name = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Comments(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    Comment = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.Comment

class Resources(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='resources')
    resource = models.TextField()
    def __str__(self):
        return self.resource

class TaskRuleAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    rule = models.ForeignKey('automation.AutomationRule', on_delete=models.CASCADE)
