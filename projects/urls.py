from django.urls import path,include
from projects.views import ProjectDashboard
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('', ProjectDashboard)

urlpatterns = [
    path('', include(router.urls)),
]
