from rest_framework import permissions

class IsAdminOrProjectManager(permissions.BasePermission):
    """
    Allows full access to Admins/PMs, Read-only for others.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser or getattr(request.user, 'is_project_manager', False)