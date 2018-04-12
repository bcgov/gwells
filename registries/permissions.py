"""
Registries view permission classes
"""

from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS


class IsAdminOrReadOnly(IsAdminUser):
    """
    Allows read-only access to all users (including anonymous users) and write access to admin users only
    """

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return is_admin or request.method in SAFE_METHODS


class IsGwellsAdmin(BasePermission):
    """
    Grants permission to users with the is_gwells_admin flag (supplied by Keycloak)
    """

    def has_permission(self, request, view):
        # user is a gwells admin (comes from Keycloak role)
        is_gwells_admin = (
            request.user and
            request.user.is_authenticated and
            request.user.profile and
            request.user.profile.is_gwells_admin)

        # user is an admin (comes from Django's default user model is_staff)
        is_system_admin = (
            request.user and
            request.user.is_authenticated and
            request.user.is_staff)

        return is_gwells_admin or is_system_admin
