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

from django.contrib.auth.models import Group, Permission

# Keycloak/SSO groups:
ADJUDICATOR_ROLE = 'gwells_adjudicator'
AUTHORITY_ROLE = 'gwells_statutory_authority'
ADMIN_ROLE = 'gwells_admin'
VIEWER_ROLE = 'gwells_viewer'

ADJUDICATOR_GROUP_NAME = 'gwells_adjudicator'
AUTHORITY_GROUP_NAME = 'gwells_authority'
ADMIN_GROUP_NAME = 'gwells_admin'
VIEWER_GROUP_NAME = 'gwells_viewer'

ROLE_MAP = {
    ADJUDICATOR_ROLE: ADJUDICATOR_GROUP_NAME,
    AUTHORITY_ROLE: AUTHORITY_GROUP_NAME,
    ADMIN_ROLE: ADMIN_GROUP_NAME,
    VIEWER_ROLE: VIEWER_GROUP_NAME
}

GWELLS_ROLES = (ADJUDICATOR_ROLE, AUTHORITY_ROLE, ADMIN_ROLE, VIEWER_ROLE)
GWELLS_ROLE_GROUPS = (
    ROLE_MAP[ADJUDICATOR_ROLE],
    ROLE_MAP[AUTHORITY_ROLE],
    ROLE_MAP[ADMIN_ROLE],
    ROLE_MAP[VIEWER_ROLE]
)


def roles_to_groups(user, roles=None):
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

    # Default permissions for Application Administrators
    ADMIN_PERMISSIONS = [x for x in
                         Permission.objects.filter(codename__in=['add_person',
                                                                 'change_person',
                                                                 'delete_person',
                                                                 'add_organization',
                                                                 'change_organization',
                                                                 'delete_organization',
                                                                 'add_registriesapplication',
                                                                 'change_registriesapplication',
                                                                 'delete_registriesapplication',
                                                                 'add_register',
                                                                 'change_register',
                                                                 'delete_register',
                                                                 'add_personnote',
                                                                 'change_personnote',
                                                                 'delete_personnote',
                                                                 'add_organizationnote',
                                                                 'change_organizationnote',
                                                                 'delete_organizationnote'])
                         ]

    # Default permissions for Adjudicator and Statutory Authority roles
    ADJUDICATOR_PERMISSIONS = ADMIN_PERMISSIONS
    AUTHORITY_PERMISSIONS = ADMIN_PERMISSIONS
    VIEWER_PERMISSIONS = []

    PERMISSION_MAP = {
        ADJUDICATOR_ROLE: ADJUDICATOR_PERMISSIONS,
        AUTHORITY_ROLE: AUTHORITY_PERMISSIONS,
        ADMIN_ROLE: ADMIN_PERMISSIONS,
        VIEWER_ROLE: VIEWER_PERMISSIONS
    }

    if user is None:
        raise exceptions.AuthenticationFailed(
            'Failed to retrieve user to apply roles to')

    user_group_names = [group.name for group in user.groups.all()]

    for role in roles:

        # if user is not in their role group, add them
        if role in GWELLS_ROLES and ROLE_MAP.get(role) not in user_group_names:
            group, created = Group.objects.get_or_create(
                name=ROLE_MAP.get(role))
            group.user_set.add(user)
            if created:
                group.permissions.set(PERMISSION_MAP.get(role))

    # check if user has been removed from their SSO (Keycloak) group
    for group in user_group_names:
        if (group in GWELLS_ROLE_GROUPS and
                group not in [ROLE_MAP.get(role) for role in roles] and
                user.groups.filter(name=group).exists()):
            user.groups.get(name=group).user_set.remove(user)
