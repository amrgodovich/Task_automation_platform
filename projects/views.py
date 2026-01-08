from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework import status
from projects.models import Project
from projects.serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticated

# class ProjectDashboardView(views.APIView):
    
#     def get(self, request):
#         if request.user.is_anonymous:
#             return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
#         projects = Project.objects.filter(owner=request.user)
#         serializer = ProjectSerializer(projects, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = ProjectSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDashboard(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)