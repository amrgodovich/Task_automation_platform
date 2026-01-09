from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectDashboard, UsersOfProjectViewSet

router = DefaultRouter()
router.register('', ProjectDashboard, basename='project')

urlpatterns = [
    path('<int:project_id>/users/', UsersOfProjectViewSet.as_view({'get': 'list'}), name='project-users'),
    path('', include(router.urls)),
    
]