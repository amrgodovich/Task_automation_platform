from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework import status
from projects.models import Project
from projects.serializers import ProjectSerializer, ProjectMemberSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPMorNormal


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