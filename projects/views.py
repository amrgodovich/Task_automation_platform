from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework import status
from projects.models import Project
from projects.serializers import ProjectSerializer, ProjectMemberSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly


class ProjectDashboard(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_queryset(self):
        return Project.objects.filter(members__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)