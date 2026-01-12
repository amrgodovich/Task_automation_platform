from django.contrib import admin
from .models import Task, Milestone, Comments, TaskRuleAssignment
# Register your models here.
admin.site.register(Task)
admin.site.register(Milestone)
admin.site.register(Comments)
admin.site.register(TaskRuleAssignment)