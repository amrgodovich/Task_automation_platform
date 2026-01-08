from django.contrib import admin
from .models import Trigger, Action, JobExecution
# Register your models here.

admin.site.register(Trigger)
admin.site.register(Action)
admin.site.register(JobExecution)