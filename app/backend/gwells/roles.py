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


# Keycloak/SSO roles - these map to Django groups.
ADMIN_ROLE = 'gwells_admin'
# TODO: The ADJUDICATOR and AUTHORITY role should be removed. These concepts should exist as groups in
#           keycloak, and the underlying actions should be defined as roles seperate from business rules.
#           e.g.: an adjudicator may view and edit registries.
REGISTRIES_ADJUDICATOR_ROLE = 'registries_adjudicator'
REGISTRIES_AUTHORITY_ROLE = 'registries_statutory_authority'
REGISTRIES_VIEWER_ROLE = 'registries_viewer'
WELLS_VIEWER_ROLE = 'wells_viewer'
WELLS_EDIT_ROLE = 'wells_edit'

# These roles are excluded, as they cannot be mapped to any particular useful groups.
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
            group = Group.objects.filter(name=role).first()
            if not group:
                # From time to time, a new role will be added to keycloak, and this role will not yet
                # exist in the django database as a group. When this happens, we create it.
                logger.error('Group "{}" does not exist. Creating it....'.format(role))
                group = Group(name=role)
                group.save()
            group.user_set.add(user)

    # check if user has been removed from their SSO (Keycloak) group
    for group in user_group_names:
        if group not in roles:
            user.groups.get(name=group).user_set.remove(user)
