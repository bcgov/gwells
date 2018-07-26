"""
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
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
