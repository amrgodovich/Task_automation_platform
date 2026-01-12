from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectDashboard, UsersOfProjectViewSet
from tasks.views import TaskViewSet, TaskMembersViewSet, TaskMilestonesViewSet, TaskCommentsViewSet, TaskResourcesViewSet

router = DefaultRouter()
router.register('', ProjectDashboard, basename='project')

task_router = DefaultRouter()
task_router.register(r'', TaskViewSet, basename='project-tasks')

urlpatterns = [
    # Project Members
    path('<int:project_id>/users/', UsersOfProjectViewSet.as_view({'get': 'list'}), name='project-users'),

    # Task-Specific Nested Resources
    # These paths follow the pattern: projects/<pid>/tasks/<tid>/resource/
    path('<int:project_id>/tasks/<int:task_id>/members/', TaskMembersViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-members'),
    
    path('<int:project_id>/tasks/<int:task_id>/milestones/', TaskMilestonesViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-milestones'),
    path('<int:project_id>/tasks/<int:task_id>/milestones/<int:pk>/', TaskMilestonesViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='task-milestone-detail'),

    path('<int:project_id>/tasks/<int:task_id>/comments/', TaskCommentsViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-comments'),
    
    path('<int:project_id>/tasks/<int:task_id>/resources/', TaskResourcesViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-resources'),

    # Task List and Detail (e.g., /projects/1/tasks/ and /projects/1/tasks/22/)
    path('<int:project_id>/tasks/', include(task_router.urls)),

    # Main Project Routes
    path('', include(router.urls)),
]