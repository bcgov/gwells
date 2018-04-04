from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER

class JwtOidcAuthentication(JSONWebTokenAuthentication):
    """
    Authenticate users who provide a JSON Web Token in the request headers (e.g. Authorization: JWT xxxxxxxxxx)
    """

    def authenticate_credentials(self, payload):
        User = get_user_model()
        username = payload.get('sub')

        if username is None:
            raise exceptions.AuthenticationFailed('JWT did not contain a "sub" attribute')

        try:
            user = User.objects.get_or_create(user=username)
        
        except:
            raise exceptions.AuthenticationFailed('Failed to retrieve or create user')
        
        return user
