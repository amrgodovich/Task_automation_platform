from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework import status
from projects.models import Project, ProjectMember
from projects.serializers import ProjectSerializer, ProjectMemberSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPMorNormal
from django.shortcuts import get_object_or_404

class ProjectDashboard(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsPMorNormal]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Project.objects.all()
        return Project.objects.filter(members__user=self.request.user).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UsersOfProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsAuthenticated, IsPMorNormal]

    def get_queryset(self):
        return ProjectMember.objects.filter(
            project_id=self.kwargs.get('project_id')
        ).select_related('user')

    def list(self, request, *args, **kwargs):
        project = get_object_or_404(Project, project_id=self.kwargs.get('project_id'))

        if not (request.user.is_superuser or project.owner == request.user):
            return Response(
                {"detail": "Not authorized to view members of this project."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        return super().list(request, *args, **kwargs)