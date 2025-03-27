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
from django.db.utils import IntegrityError


logger = logging.getLogger(__name__)


# Keycloak/SSO roles - these map to Django groups.
# The concept of groups such as "Registries Statutory Authority" exists only in Keycloak. The groups
# defined in keycloak contain a number of keyloak rules. Those keycloak roles in turn, get mapped to django
# groups.
REGISTRIES_EDIT_ROLE = 'registries_edit'
REGISTRIES_VIEWER_ROLE = 'registries_viewer'
# REGISTRIES_APPROVE_ROLE = 'registries_approve' <-- this is a planned, unimplemented role
WELLS_VIEWER_ROLE = 'wells_viewer'
WELLS_EDIT_ROLE = 'wells_edit'
WELLS_SUBMISSION_ROLE = 'wells_submission'
WELLS_SUBMISSION_VIEWER_ROLE = 'wells_submission_viewer'
# WELLS_APPROVE_ROLE = 'wells_approve' <-- this is a planned, unimplemented role
AQUIFERS_VIEWER_ROLE = 'aquifers_view'
AQUIFERS_EDIT_ROLE = 'aquifers_edit'

BULK_WELL_AQUIFER_CORRELATION_UPLOAD = 'bulk_well_aquifer_correlation_upload'
BULK_AQUIFER_DOCUMENTS_UPLOAD = 'bulk_aquifer_documents_upload'
BULK_VERTICAL_AQUIFER_EXTENTS_UPLOAD = 'bulk_vertical_aquifer_extents_upload'

# Surveys
SURVEYS_EDIT_ROLE = 'surveys_edit'

# IDIR
IDIR_ROLE = 'idir'

# These roles are excluded, as they cannot be mapped to any particular useful groups.
EXCLUDE = ('offline_access', 'admin', 'uma_authorization', 'gwells_admin')


def roles_to_groups(user, roles: Tuple[str] = None):
    """
    Add users to groups based on roles from single sign-on identity provider

    Business role for registries:
      adjudicator: e.g. Groundwater Data Specialist
        Enters applications for new or existing registrants.
          read/write access to: Person, Organization, Application, Registration

      authority: e.g. Deputy Comptroller
        Approves changes to application or registration status
          read/write access to: Person, Organization, Application, Registration,
            ApplicationStatus, RegistrationStatus

      viewer: e.g. Groundwater Protection Officer
          read only access to: Person, Organization, Application, Registration

    Business roles for aquifers:
        TBD

    Business roles for wells and submissions:
        TBD

    """
    if user is None:
        raise exceptions.AuthenticationFailed(
            'Failed to retrieve user to apply roles to')

    user_group_names = [group.name for group in user.groups.all()]

    role_change = False

    for role in roles:
        # if user is not in their role group, add them
        if role not in user_group_names and role not in EXCLUDE:
            # When a role/group is newly assigned, there may be many parallel processes that try to add
            # a create a group, and add a user to a group.
            # We don't want to lock - that can slow everything down. If there's an integrity error,
            # we don't really care either, it just means someone beat us to it, so we don't allow the
            # exception to bubble up, we just log it.
            # This is an unfortunate side effect of how we've decided to handle sso->django integration.
            group = Group.objects.filter(name=role).first()
            if not group:
                # From time to time, a new role will be added to keycloak, and this role will not yet
                # exist in the django database as a group. When this happens, we create it.
                logger.info('Group "{}" does not exist. Creating it....'.format(role))
                group = Group(name=role)
                try:
                    group.save()
                except IntegrityError as e:
                    logger.info(e)
                    # In the time we tried to create this group, someone may have beat us to it! Try to
                    # reload it again.
                    group = Group.objects.filter(name=role).first()
                    if not group:
                        # Uh oh - can't create it, can't load it - out of ideas!
                        raise
            try:
                group.user_set.add(user)
            except IntegrityError as e:
                logger.info(e)
            role_change = True

    # check if user has been removed from their SSO (Keycloak) group
    for group in user_group_names:
        if group not in roles:
            user.groups.get(name=group).user_set.remove(user)
            role_change = True

    if role_change:
        user.refresh_from_db()
