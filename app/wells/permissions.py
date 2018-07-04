from rest_framework.permissions import DjangoModelPermissions
from gwells.roles import WELLS_ROLES


class WellsPermissions(DjangoModelPermissions):
    """
    Grants permissions to users based on Django model permissions
    """

    def has_permission(self, request, view):
        """
        Refuse permission if user is not GWELLS staff
        """
        if request.user and request.user.is_authenticated and request.user.groups.filter(
                name__in=WELLS_ROLES).exists():
            return True
        return False
