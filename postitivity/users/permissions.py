from rest_framework import permissions

class IsAdminOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view): 
        if request.method == 'POST':   # Allow anyone to create an account (POST)
            return True 
        return request.user and request.user.is_superuser # Only admin/superuser can view list (GET)

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admin/superuser can do anything
        if request.user and request.user.is_superuser:
            return True
        # For GET requests, also check if user is owner
        if request.method in permissions.SAFE_METHODS:
            return obj == request.user
        # For other methods, check if user is owner
        return obj == request.user