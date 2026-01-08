from django.urls import path,include
from users.views import UserManagementViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('', UserManagementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
