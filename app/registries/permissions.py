"""
Registries view permission classes
"""

from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS, DjangoModelPermissions


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


class GwellsPermissions(DjangoModelPermissions):
    """
    Grants permissions to users based on Django model permissions, with additional check for
    user's status as GWELLS staff
    """

    def has_permission(self, request, view):
        """
        Refuse permission entirely if user is not GWELLS staff, else continue to check model-level permissions
        This is used to refuse permission for viewing data for non-staff (but authenticated) users
        """
        if not request.user or not request.user.is_authenticated or not request.user.profile.is_gwells_admin:
            return False
        return super(GwellsPermissions, self).has_permission(request, view)
