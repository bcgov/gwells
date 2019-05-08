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
from datetime import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from gwells.models import Profile
from gwells.roles import roles_to_groups


class JwtOidcAuthentication(JSONWebTokenAuthentication):
    """
    Authenticate users who provide a JSON Web Token in the request headers (e.g. Authorization: JWT xxxxxxxxx)
    """

    def authenticate_credentials(self, payload):
        User = get_user_model()
        # Get keycloak ID from JWT token
        username = payload.get('sub')
        if username is None:
            raise exceptions.AuthenticationFailed(
                'JWT did not contain a "sub" attribute')

        # Make sure the preferred username contains either idir\ or bceid\
        # so we know that the user is coming from a known sso authority
        if not self.known_sso_authority(payload):
            raise exceptions.AuthenticationFailed(
                'Preferred username is invalid.')

        # There are various values we can get from the Token, we don't technically need most of them,
        # but they are useful to put in the user table for debugging purposes.
        payload_user_mapping = {
            'email': 'email',
            'family_name': 'last_name'
        }
        payload_profile_mapping = {
            'preferred_username': 'username',
            'name': 'name'
        }
        # We map auth_time to user.last_login ; this is true depending on your point of view. It's the
        # last time the user logged into sso, which may not co-incide with the last time the user
        # logged into gwells.
        auth_time = payload.get('auth_time')
        if auth_time:
            auth_time = datetime.fromtimestamp(auth_time, tz=timezone.utc)

        # Get or create a user with the keycloak ID.
        try:
            user, update = User.objects.get_or_create(username=username)
        except:
            raise exceptions.AuthenticationFailed(
                'Failed to retrieve or create user')

        if update:
            # User created, set various values for the 1'st time.
            user.set_password(User.objects.make_random_password(length=36))

        # If one of these attributes has changed - do an update.
        for source, target in payload_user_mapping.items():
            value = payload.get(source)
            if value and value != getattr(user, target):
                update = True
                setattr(user, target, value)
        if auth_time and user.last_login != auth_time:
            update = True
            user.last_login = auth_time
        if update:
            user.save()

        # Load the user's GWELLS profile.
        try:
            profile, update = Profile.objects.get_or_create(user=user.id)
        except:
            raise exceptions.AuthenticationFailed(
                'Failed to create user profile')

        for source, target in payload_profile_mapping.items():
            value = payload.get(source)
            if value and value != getattr(profile, target):
                update = True
                if source == 'preferred_username':
                    value = value.upper()  # Uppercase to match existing data
                setattr(profile, target, value)
        if not profile.name and profile.username:
            # When the name of the user isn't available, fallback to the username
            profile.name = profile.username
            update = True
        if update:
            profile.save()

        # Get the roles supplied by Keycloak for this user.
        try:
            roles = payload.get('realm_access').get('roles')
        except:
            raise exceptions.AuthenticationFailed('Failed to retrieve roles')

        # Put user in groups based on role.
        roles_to_groups(user, roles)

        return user

    @staticmethod
    def known_sso_authority(payload):
        preferred_username = payload.get('preferred_username')
        return 'idir\\' in preferred_username or 'bceid\\' in preferred_username\
            or preferred_username == 'testuser'
