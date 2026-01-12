from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NotificationEventViewSet, 
    MessageTemplateViewSet, 
    AutomationRuleViewSet
)

router = DefaultRouter()
router.register(r'events', NotificationEventViewSet, basename='notification-event')
router.register(r'templates', MessageTemplateViewSet, basename='message-template')
router.register(r'rules', AutomationRuleViewSet, basename='automation-rule')

urlpatterns = [
    path('', include(router.urls)),
]