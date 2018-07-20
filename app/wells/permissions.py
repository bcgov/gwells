from rest_framework.permissions import DjangoModelPermissions, BasePermission
from gwells.roles import WELLS_ROLES


class WellsDocumentPermissions(BasePermission):
    """
    Grants permission to view documents to users in a Wells staff group
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.groups.filter(
                name__in=WELLS_ROLES).exists():
            return True
        return False


class WellsPermissions(DjangoModelPermissions):
    """
    Grants permissions to users based on Django model permissions
    """

    def has_permission(self, request, view):
        """
        Refuse permission if user is not in a "Wells" staff group.
        If user in one of the wells groups, group permissions will dictate (e.g. user is
        in a group that has 'add_well' permission)
        """
        if request.user and request.user.is_authenticated and request.user.groups.filter(
                name__in=WELLS_ROLES).exists():
            return super().has_permission(request, view)
        return False
