from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        print(f"User: {request.user}, Role: {getattr(request.user, 'role', None)}")  # Debug role
        if request.method == "POST":
            return request.user.is_authenticated and request.user.role == "admin"
        return request.user.is_authenticated
