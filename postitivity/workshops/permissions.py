from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and (request.user.is_superuser or request.user.is_staff)

class IsAdminOwnerOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Step 1: Allow anyone to view
        if request.method == 'GET':
            return True
        
        # Step 2: Must be logged in to create/edit
        if not request.user.is_authenticated:
            return False

        # Step 3: If superuser, allow everything
        if request.user.is_superuser:
            return True

        # Step 4: If admin, check ownership in has_object_permission
        if request.user.is_staff:
            return True

        # Step 5: Regular users - allow note creation but not workshop creation
        if view.__class__.__name__ == 'Notelist':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Step 1: If superuser, allow everything
        if request.user.is_superuser:
            return True

        # Step 2: If admin, check if they own the workshop
        if request.user.is_staff:
            if type(obj).__name__ == 'Workshop':
                return obj.created_by_user == request.user
            if type(obj).__name__ == 'Notes':
                return obj.workshop.created_by_user == request.user

        # Step 3: Regular users can edit their own notes
        if type(obj).__name__ == 'Notes':
            return obj.user == request.user

        # Step 4: Regular users can't edit anything else
        return False
    

class IsSuperUserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser