from rest_framework import serializers
from projects.models import Project,ProjectMember
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Project
        fields = '__all__'

class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_project_manager','profile_picture']

class ProjectMemberSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only=True)
    class Meta:
        model = ProjectMember
        fields = '__all__'
        # fields = ['id', 'role', 'joined_at', 'project', 'user']
    
