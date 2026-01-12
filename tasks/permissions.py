from rest_framework import permissions
from projects.models import ProjectMember

class IsPM(permissions.BasePermission):
    """
    Allows access only to project members or superusers.
    """
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_id')
        if not project_id:
            return False
        
        if request.user.is_superuser:
            return True

        return ProjectMember.objects.filter(
            project_id=project_id, 
            user=request.user
        ).exists()

class IsAuthorOrPM(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object or 
    the project owner to edit/delete it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        is_author = getattr(obj, 'user', None) == request.user
        
        # Check if the user is the owner of the project associated with the task
        project_owner = False
        if hasattr(obj, 'task'):
            project_owner = obj.task.project.owner == request.user
        elif hasattr(obj, 'project'):
            project_owner = obj.project.owner == request.user

        return is_author or project_owner or request.user.is_superuser