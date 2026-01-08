from rest_framework import permissions

class IsPMorNormal(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # 2. Restrict Create (POST) to Superusers OR Project Managers
        if request.method == 'POST':
            return request.user.is_authenticated and (
                request.user.is_superuser or getattr(request.user, 'is_project_manager', False)
            )

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.owner == request.user
        return True