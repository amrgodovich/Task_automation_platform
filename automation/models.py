from django.db import models


# class RecipientRoles(models.TextChoices):
#     ADMIN = 'ADMIN', 'System Admin'
#     MANAGER = 'MANAGER', 'Project Manager'
#     MEMBER = 'MEMBER', 'Team Member'

# 1. THE PURPOSE (Catalog)
class NotificationEvent(models.Model):
    code = models.CharField(max_length=50, unique=True) # e.g. "COMMENT_ADDED"
    description = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.description}"

# 2. THE CONTENT (Templates)
class MessageTemplate(models.Model):
    class ChannelTypes(models.TextChoices):
        EMAIL = 'EMAIL', 'Email'
        IN_APP = 'NOTIFICATION', 'In-App Notification'
        ALL = 'ALL', 'Default (All Channels)'
    event = models.ForeignKey(NotificationEvent, on_delete=models.CASCADE)
    # If channel is ALL, this text is used for everything. 
    # If channel is EMAIL, this specific template is used only for emails.
    channel = models.CharField(max_length=20, choices=ChannelTypes.choices, default=ChannelTypes.ALL)
    
    subject_template = models.CharField(max_length=200) 
    body_template = models.TextField() # "User {{ user }} commented: {{ text }}"

    class Meta:
        unique_together = ('event', 'channel') # One template per channel per event

# 3. THE DISTRIBUTION (Rules)
class AutomationRule(models.Model):
    title = models.CharField(max_length=100, default="")
    event = models.ForeignKey(NotificationEvent, on_delete=models.CASCADE)
    
    # Who gets it?
    recipients = models.JSONField(default=list) # e.g. ["MANAGER", "MEMBER"]
    
    # How do they get it?
    channels = models.JSONField(default=list) # e.g. ["EMAIL", "IN_APP"]

    def __str__(self):
        return f"{self.title}"