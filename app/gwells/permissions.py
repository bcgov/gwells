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


# Default permissions for Application Administrators
ADMIN_PERMISSIONS = [
    Permission.objects.get(codename='add_person'),
    Permission.objects.get(codename='change_person'),
    Permission.objects.get(codename='delete_person'),
    Permission.objects.get(codename='add_organization'),
    Permission.objects.get(codename='change_organization'),
    Permission.objects.get(codename='delete_organization'),
    Permission.objects.get(codename='add_registriesapplication'),
    Permission.objects.get(codename='change_registriesapplication'),
    Permission.objects.get(codename='delete_registriesapplication'),
    Permission.objects.get(codename='add_register'),
    Permission.objects.get(codename='change_register'),
    Permission.objects.get(codename='delete_register'),
    Permission.objects.get(codename='add_personnote'),
    Permission.objects.get(codename='change_personnote'),
    Permission.objects.get(codename='delete_personnote'),
    Permission.objects.get(codename='add_organizationnote'),
    Permission.objects.get(codename='change_organizationnote'),
    Permission.objects.get(codename='delete_organizationnote'),
]

# Default permissions for Data Entry Specialists and Deputy Comptrollers
ADJUDICATOR_PERMISSIONS = ADMIN_PERMISSIONS
AUTHORITY_PERMISSIONS = ADMIN_PERMISSIONS


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

    # create/retrieve groups and, if group is new, set permissions for groups
    authority_group, authority_group_created = Group.objects.get_or_create(
        name=AUTHORITY_GROUP_NAME)
    if authority_group_created:
        authority_group.permissions.set(AUTHORITY_PERMISSIONS)

    adjudicator_group, adjudicator_group_created = Group.objects.get_or_create(
        name=ADJUDICATOR_GROUP_NAME)
    if adjudicator_group_created:
        adjudicator_group.permissions.set(ADJUDICATOR_PERMISSIONS)

    admin_group, admin_group_created = Group.objects.get_or_create(
        name=ADMIN_GROUP_NAME)
    if admin_group_created:
        admin_group.permissions.set(ADMIN_PERMISSIONS)

    viewer_group, viewer_group_created = Group.objects.get_or_create(
        name=VIEWER_GROUP_NAME)

    if user is None:
        raise exceptions.AuthenticationFailed('User groups not configured')

    # user_is_staff will be set to True if user in one of the staff groups
    user_is_staff = False

    # add or remove user from Comptroller group
    if AUTHORITY_ROLE in roles:
        authority_group.user_set.add(user)
        user_is_staff = True

    elif user.groups.filter(name=authority_group.name).exists():
        authority_group.user_set.remove(user)

    # add or remove user from Data Specialist group
    if ADJUDICATOR_ROLE in roles:
        adjudicator_group.user_set.add(user)
        user_is_staff = True

    elif user.groups.filter(name=adjudicator_group.name).exists():
        adjudicator_group.user_set.remove(user)

    # add or remove user from Admin group
    if ADMIN_ROLE in roles:
        admin_group.user_set.add(user)
        user_is_staff = True

    elif user.groups.filter(name=admin_group.name).exists():
        admin_group.user_set.remove(user)

    # add or remove user from Officer group
    if VIEWER_ROLE in roles:
        viewer_group.user_set.add(user)
        user_is_staff = True

    elif user.groups.filter(name=viewer_group.name).exists():
        viewer_group.user_set.remove(user)

    if user_is_staff:
        user.profile.is_gwells_admin = True
        user.profile.save()

    else:
        user.profile.is_gwells_admin = False
        user.profile.save()
