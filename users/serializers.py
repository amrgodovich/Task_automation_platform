from rest_framework import serializers
from users.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'is_superuser', 'is_staff', 'is_project_manager','profile_picture']
        read_only_fields = ['id']
        