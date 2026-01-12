from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import NotificationEvent, MessageTemplate, AutomationRule
from .serializers import NotificationEventSerializer,  MessageTemplateSerializer, AutomationRuleSerializer
from .permissions import IsAdminOrProjectManager

class NotificationEventViewSet(viewsets.ModelViewSet):
    queryset = NotificationEvent.objects.all()
    serializer_class = NotificationEventSerializer
    permission_classes = [IsAuthenticated, IsAdminOrProjectManager]

class MessageTemplateViewSet(viewsets.ModelViewSet):
    queryset = MessageTemplate.objects.all()
    serializer_class = MessageTemplateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrProjectManager]
    
    def get_queryset(self):
        # Allow filtering templates by event code
        event_code = self.request.query_params.get('event_code')
        if event_code:
            return self.queryset.filter(event__code=event_code)
        return self.queryset

class AutomationRuleViewSet(viewsets.ModelViewSet):
    queryset = AutomationRule.objects.all()
    serializer_class = AutomationRuleSerializer
    permission_classes = [IsAuthenticated, IsAdminOrProjectManager]