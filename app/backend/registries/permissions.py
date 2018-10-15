"""
Registries view permission classes
"""

from django.db.models import Q
from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS, DjangoModelPermissions

from gwells.roles import REGISTRIES_ADJUDICATOR_ROLE, REGISTRIES_AUTHORITY_ROLE


class IsAdminOrReadOnly(IsAdminUser):
    """
    Allows read-only access to all users (including anonymous users) and write access to admin users only
    """

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return is_admin or request.method in SAFE_METHODS


class RegistriesPermissions(DjangoModelPermissions):
    """
    Grants permissions to users based on Django model permissions
    """

    def has_permission(self, request, view):
        """
        Refuse permission entirely if user is not GWELLS staff, else continue to check model-level permissions
        This is used to refuse permission for viewing data for non-staff (but authenticated) users
        """
        if not request.user or not request.user.is_authenticated or not request.user.groups.filter(
                Q(name=REGISTRIES_ADJUDICATOR_ROLE) | Q(name=REGISTRIES_AUTHORITY_ROLE)).exists():
            return False
        return super().has_permission(request, view)
