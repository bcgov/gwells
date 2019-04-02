"""
Registries view permission classes
"""

from django.db.models import Q
from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS, BasePermission

from gwells.roles import REGISTRIES_EDIT_ROLE, REGISTRIES_VIEWER_ROLE


class RegistriesEditOrReadOnly(BasePermission):
    """
    Allows read-only access to all users (including anonymous users) and write access to users with
    edit rights.
    """

    def has_permission(self, request, view):
        has_edit = request.user and request.user.is_authenticated and request.user.groups.filter(
            name=REGISTRIES_EDIT_ROLE).exists()
        result = has_edit or request.method in SAFE_METHODS
        return result


class RegistriesEditPermissions(BasePermission):

    def has_permission(self, request, view):
        """
        - Refuses permission entirely if user is not GWELLS staff with edit role.
        - Allows users with view rights to access safe methods.
        - Allows users with edit rights to access all other methods.
        """
        has_edit = request.user and request.user.is_authenticated and request.user.groups.filter(
            name=REGISTRIES_EDIT_ROLE).exists()
        has_view = request.user and request.user.is_authenticated and request.user.groups.filter(
            name=REGISTRIES_VIEWER_ROLE).exists()
        return has_edit or (has_view and request.method in SAFE_METHODS)
