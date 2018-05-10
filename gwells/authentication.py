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

from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from gwells.models.Profile import Profile


class JwtOidcAuthentication(JSONWebTokenAuthentication):
    """
    Authenticate users who provide a JSON Web Token in the request headers (e.g. Authorization: JWT xxxxxxxxxx)
    """

    def authenticate_credentials(self, payload):
        User = get_user_model()

        # get keycloak ID from JWT token
        username = payload.get('sub')

        if username is None:
            raise exceptions.AuthenticationFailed(
                'JWT did not contain a "sub" attribute')

        # get or create a user with the keycloak ID
        try:
            user, user_created = User.objects.get_or_create(username=username)
        except:
            raise exceptions.AuthenticationFailed(
                'Failed to retrieve or create user')

        if user_created:
            user.set_password(User.objects.make_random_password(length=36))
            user.email = payload.get('email')
            user.save()

        user.email = payload.get('email')
        user.save()

        # load the user's GWELLS profile
        try:
            profile, __ = Profile.objects.get_or_create(user=user.id)
        except:
            raise exceptions.AuthenticationFailed(
                'Failed to create user profile')

        # get the roles supplied by Keycloak for this user
        try:
            roles = payload.get('realm_access').get('roles')
        except:
            raise exceptions.AuthenticationFailed('Failed to retrieve roles')

        if 'gwells_admin' in roles:
            profile.is_gwells_admin = True
            profile.save()
            user.is_staff = True
            user.save()

        # get the name from the token and store it in the profile. If name not supplied, use the username.
        name = payload.get('name') or payload.get('preferred_username')
        profile.name = name
        profile.save()

        return user
