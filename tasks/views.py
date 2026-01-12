from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Task, TaskMember,Milestone, Comments, Resources
from projects.models import Project
from .serializers import TaskSerializer, TaskMemberSerializer,MillstoneSerializer, CommentsSerializer, ResourcesSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        return Task.objects.filter(project_id=self.kwargs.get('project_id'))

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs.get('project_id'))
        serializer.save(project=project)

class TaskMembersViewSet(viewsets.ModelViewSet):
    serializer_class = TaskMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TaskMember.objects.filter(
            task_id=self.kwargs.get('task_id')
        ).select_related('user')

    # def list(self, request, *args, **kwargs):
    #     task = get_object_or_404(Task, pk=self.kwargs.get('task_id'))
        
    #     if not (request.user.is_superuser or task.project.owner == request.user):
    #         return Response(
    #             {"detail": "Not authorized to view members of this task."}, 
    #             status=status.HTTP_403_FORBIDDEN
    #         )
    #     return super().list(request, *args, **kwargs)

class TaskMilestonesViewSet(viewsets.ModelViewSet):
    serializer_class = MillstoneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Milestone.objects.filter(
            task_id=self.kwargs.get('task_id')
        )

class TaskCommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comments.objects.filter(
            task_id=self.kwargs.get('task_id')
        )
    def perform_create(self, serializer):
        task = get_object_or_404(Task, pk=self.kwargs.get('task_id'))
        serializer.save(task=task, user=self.request.user)

class TaskResourcesViewSet(viewsets.ModelViewSet):
    serializer_class = ResourcesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Resources.objects.filter(
            task_id=self.kwargs.get('task_id')
        )