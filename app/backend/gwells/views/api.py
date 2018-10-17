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


class GeneralConfig(APIView):
    """ serves general configuration """

    def get(self, request):
        config = {
            "enable_data_entry": get_env_variable("ENABLE_DATA_ENTRY") == "True",
            "enable_google_analytics": get_env_variable("ENABLE_GOOGLE_ANALYTICS") == "True",
            "enable_aquifers_search": get_env_variable("ENABLE_AQUIFERS_SEARCH") == "True",
            "sso_idp_hint": get_env_variable("SSO_IDP_HINT", "idir")
        }
        return Response(config)
