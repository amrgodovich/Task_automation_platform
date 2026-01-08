from rest_framework import viewsets, permissions, exceptions
from .models import UserProfile
from .serializers import UserSerializer

class UserManagementViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = UserProfile.objects.all()
    
    def get_permissions(self):
        # ONLYYYY Superusers and PMs can access this endpoint
        if self.request.user.is_superuser:
            return [permissions.IsAuthenticated()]

        raise exceptions.PermissionDenied("You do not have authority to manage users.")

    def perform_create(self, serializer):
        # we force the new user to be a standard normal user.
        serializer.save(
            is_superuser=False,
            is_staff=False,
            is_project_manager=False
        )