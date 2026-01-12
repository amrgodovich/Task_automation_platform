from rest_framework import serializers
from .models import NotificationEvent, MessageTemplate, AutomationRule

class NotificationEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationEvent
        fields = '__all__'

class MessageTemplateSerializer(serializers.ModelSerializer):
    event_name = serializers.ReadOnlyField(source='event.description')
    
    class Meta:
        model = MessageTemplate
        fields = '__all__'

class AutomationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutomationRule
        fields = '__all__'