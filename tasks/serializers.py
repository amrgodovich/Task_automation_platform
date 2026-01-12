from rest_framework import serializers
from .models import Task, TaskMember, Milestone, Comments, Resources

class TaskMemberSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = TaskMember
        fields = ['id', 'user', 'user_email', 'joined_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['task_id', 'project', 'created_at', 'updated_at']

class MillstoneSerializer(serializers.ModelSerializer):
    class Meta:
        model =Milestone
        fields= '__all__'

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model =Comments
        fields= '__all__'

class ResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model =Resources
        fields= '__all__'