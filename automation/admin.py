from django.contrib import admin
from .models import NotificationEvent, MessageTemplate, AutomationRule


@admin.register(NotificationEvent)
class NotificationEventAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code', 'description')
@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ('event', 'channel', 'subject_template')
    list_filter = ('channel',)
    search_fields = ('subject_template', 'body_template')
@admin.register(AutomationRule)
class AutomationRuleAdmin(admin.ModelAdmin):
    list_display = ('title','event')
    search_fields = ('event__code',)