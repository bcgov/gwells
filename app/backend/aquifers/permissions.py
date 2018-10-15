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
from rest_framework.permissions import BasePermission, SAFE_METHODS
from gwells.roles import AQUIFERS_EDIT_ROLES

class HasAquiferEditRoleOrReadOnly(BasePermission):
    """
    Grants permission to users with Aquifer Edit Roles, or is a read-only request
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name__in=AQUIFERS_EDIT_ROLES).exists()
        )
