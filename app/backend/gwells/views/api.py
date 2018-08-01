from rest_framework.response import Response
from rest_framework.views import APIView

from gwells.settings.base import get_env_variable


class KeycloakConfig(APIView):
    """ serves keycloak config """

    def get(self, request):
        config = {
            "realm": get_env_variable("SSO_REALM"),
            "auth-server-url": get_env_variable("SSO_AUTH_HOST"),
            "ssl-required": "external",
            "resource": get_env_variable("SSO_CLIENT"),
            "public-client": True,
            "confidential-port": int(get_env_variable("SSO_PORT", "0"))
        }
        return Response(config)
