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
from typing import Tuple
import logging

from django.contrib.auth.models import Group, Permission


logger = logging.getLogger(__name__)


# TODO: Change this section to match what's been done in Vue.js; We shouldn't have a concept of what
#       and adjudicator/admin/etc. is here. We should only be concerned with what actions can be taken.
#       Roles should be assigned appropriately to groups with keycloak.
#       On the Django level, a keycloak role, such as "registries_edit", should translate to a django_group
#       with the same name, that has the appropriate permissions set.
#       In order to affect this change, code has to be changed in this module, and a migration creating the
#       appropriate groups needs to be made.

# Keycloak/SSO roles:
ADMIN_ROLE = 'gwells_admin'
REGISTRIES_ADJUDICATOR_ROLE = 'registries_adjudicator'
REGISTRIES_AUTHORITY_ROLE = 'registries_statutory_authority'
REGISTRIES_VIEWER_ROLE = 'registries_viewer'
WELLS_VIEWER_ROLE = 'wells_viewer'
WELLS_EDIT_ROLE = 'wells_edit'
AQUIFERS_VIEWER_ROLE = 'aquifers_view'
AQUIFERS_EDIT_ROLE = 'aquifers_edit'

# Roles relating to registries.
REGISTRIES_ROLES = (
    ADMIN_ROLE,
    REGISTRIES_ADJUDICATOR_ROLE,
    REGISTRIES_AUTHORITY_ROLE,
    REGISTRIES_VIEWER_ROLE,
)

# Roles relating to wells view.
WELLS_VIEW_ROLES = (
    ADMIN_ROLE,
    WELLS_VIEWER_ROLE,
)

# Roles leating to wells edit.
WELLS_EDIT_ROLES = (
    ADMIN_ROLE,
    WELLS_VIEWER_ROLE,
    WELLS_EDIT_ROLE,
)

EXCLUDE = ('idir', 'offline_access', 'admin', 'uma_authorization')


def roles_to_groups(user, roles: Tuple[str] = None):
    """
    Add users to groups based on roles from single sign-on identity provider

    roles:
      adjudicator: e.g. Groundwater Data Specialist
        Enters applications for new or existing registrants.
          read/write access to: Person, Organization, Application, Registration

      authority: e.g. Deputy Comptroller
        Approves changes to application or registration status
          read/write access to: Person, Organization, Application, Registration,
            ApplicationStatus, RegistrationStatus

      admin: Application Administrator
        Admin for GWELLS Registries application
          read/write access to: all

      viewer: e.g. Groundwater Protection Officer
          read only access to: Person, Organization, Application, Registration

    """
    if user is None:
        raise exceptions.AuthenticationFailed(
            'Failed to retrieve user to apply roles to')

    user_group_names = [group.name for group in user.groups.all()]

    for role in roles:
        # if user is not in their role group, add them
        if role not in user_group_names and role not in EXCLUDE:
            try:
                group = Group.objects.get(name=role)
                group.user_set.add(user)
            except Group.DoesNotExist:
                logger.error('Group does not exist: {}'.format(role))

    # check if user has been removed from their SSO (Keycloak) group
    for group in user_group_names:
        if group not in roles:
            user.groups.get(name=group).user_set.remove(user)
