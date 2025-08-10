# jobs/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access for all authenticated users
        if request.method in SAFE_METHODS:
            return True
        # Only admins can write
        return request.user.is_authenticated and request.user.is_staff

