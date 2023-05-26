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
import jwt
import traceback

from datetime import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from gwells.models import Profile
from gwells.roles import roles_to_groups
from gwells.settings.base import get_env_variable
from rest_framework_jwt.settings import api_settings
from django.utils.translation import ugettext as _

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

KEYCLOAK_GOLD_REALM_URL = 'loginproxy.gov.bc.ca/auth/realms/standard'

class JwtOidcAuthentication(JSONWebTokenAuthentication):
    """
    Authenticate users who provide a JSON Web Token in the request headers (e.g. Authorization: JWT xxxxxxxxx)
    """

    def authenticate(self, payload):
        """
        (taken directly from BaseJSONWebTokenAuthentication.authenticate)

        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        jwt_value = self.get_jwt_value(payload)
        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            print(traceback.format_exc())
            msg = _('Error decoding signature.')
            
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user = self.authenticate_credentials(payload)

        return (user, jwt_value)

    def authenticate_credentials(self, payload):
        User = get_user_model()
        # Get keycloak ID (if Silver) or {guid}@{idp} (if Gold) from JWT token
        realm_user_id = payload.get('sub')
        if realm_user_id is None:
            raise exceptions.AuthenticationFailed(
                'JWT did not contain a "sub" attribute')

        # Make sure the user is coming from the same Keycloak Gold integration
        if not self.is_valid_integration(payload):
            raise exceptions.AuthenticationFailed(
                'OAuth2 audience is invalid. This can be caused by a mismatch in the SSO integration.')

        # Make sure the user is coming from a known sso authority
        if not self.known_sso_authority(payload):
            raise exceptions.AuthenticationFailed(
                'Preferred username is invalid.')

        # There are various values we can get from the Token, we don't technically need most of them,
        # but they are useful to put in the user table for debugging purposes.
        payload_user_mapping = {
            'email': 'email',
            'family_name': 'last_name'
        }

        if self.is_gold_shared_realm(payload):
            payload_profile_mapping = {
                'preferred_username': 'username',
                'name': 'name'
            }
        else:
            payload_profile_mapping = {
                'sub': 'silver_keycloak_id',
                'preferred_username': 'username',
                'name': 'name'
            }
        # We map auth_time to user.last_login ; this is true depending on your point of view. It's the
        # last time the user logged into sso, which may not co-incide with the last time the user
        # logged into gwells.
        if self.is_test_integration(payload):
            auth_time = None
        else:
            auth_time = payload.get('auth_time')
            if auth_time:
                auth_time = datetime.fromtimestamp(auth_time, tz=timezone.utc)

        # Get or create a user with the keycloak ID (if Silver) or {guid}@{idp} (if Gold).
        try:
            if self.is_gold_shared_realm(payload):
                user, update = User.objects.get_or_create(username=realm_user_id)
            else:
                # During the Gold migration process, we'll be overwriting User.username with the GUID.
                #   Prior to this, it would otherwise store the Keycloak ID.
                # But if we're still in Silver but already overwrote it, how can we retrieve users with only the KID?
                # Solution:
                #   First grab the Profile using the KID,
                #   then use profile.user_id to retrieve the User (joining on Profile.user_id = User.id).
                try:
                    profile = Profile.objects.get(silver_keycloak_id=realm_user_id)
                    user = User.objects.get(id=profile.user_id)
                    update = False
                except Profile.DoesNotExist:
                    # Profile (and therefore User) doesn't exist, so go ahead and create a new user as usual
                    user, update = User.objects.get_or_create(username=realm_user_id)
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
        # Manually combining IDP/username allows us to preserve the existing table structure meant for Silver
        if self.is_gold_shared_realm(payload):
            if self.is_test_integration(payload):
                profile.username = 'testuser'
            else:
                identity_provider = payload.get('identity_provider')
                if identity_provider == 'idir':
                    idp_username = payload.get('idir_username')
                elif identity_provider == 'bceidboth':
                    idp_username = payload.get('bceid_username')
                else:
                    # Fallback to {guid}@{idp} if it isn't IDIR or BCeID for some bizarre reason
                    profile.username = payload.get('preferred_username')
                profile.username = f'{idp_username}@{identity_provider}'.upper()
        if not profile.name and profile.username:
            # When the name of the user isn't available, fallback to the username
            profile.name = profile.username
            update = True
        if update:
            profile.save()

        # Get the roles supplied by Keycloak for this user.
        try:
            if self.is_gold_shared_realm(payload):
                roles = payload.get('client_roles')
            else:
                roles = payload.get('realm_access').get('roles')
        except:
            raise exceptions.AuthenticationFailed('Failed to retrieve roles')

        # Put user in groups based on role.
        roles_to_groups(user, roles)

        return user

    @staticmethod
    def is_gold_shared_realm(payload):
        return payload.get('iss').endswith(KEYCLOAK_GOLD_REALM_URL)

    @staticmethod
    def is_valid_integration(payload):
        return payload.get('aud') == get_env_variable('SSO_AUDIENCE') or \
               payload.get('aud') == get_env_variable('SSO_TEST_AUDIENCE')

    @staticmethod
    def is_test_integration(payload):
        return payload.get('aud') == get_env_variable('SSO_TEST_AUDIENCE')

    @staticmethod
    def known_sso_authority(payload):
        
        # Keycloak Gold has a dedicated IDP field that we can check...
        if payload.get('iss').endswith(KEYCLOAK_GOLD_REALM_URL):
            preferred_username = payload.get('preferred_username')

            if JwtOidcAuthentication.is_test_integration(payload):
                return True
            else:
                identity_provider = payload.get('identity_provider').lower()
                return identity_provider == 'idir' or identity_provider == 'bceidboth'
        # ...but Silver doesn't, so have to instead look at the preferred username, 
        # which comes in the format "{idp}\{username}"
        else:
            preferred_username = payload.get('preferred_username')
            return 'idir\\' in preferred_username or 'bceid\\' in preferred_username\
                or preferred_username == 'testuser'
