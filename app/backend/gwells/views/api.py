from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from gwells.settings.base import get_env_variable
from gwells.utils import isPointInsideBC

class KeycloakConfig(APIView):
    """ serves keycloak config """

    swagger_schema = None

    def get(self, request, **kwargs):
        config = {
            "realm": get_env_variable("SSO_REALM"),
            "auth-server-url": get_env_variable("SSO_AUTH_HOST"),
            "ssl-required": "external",
            "resource": get_env_variable("SSO_CLIENT"),
            "public-client": True,
            "confidential-port": int(get_env_variable("SSO_PORT", "0")),
            "clientId": get_env_variable("SSO_CLIENT")
        }
        return Response(config)


class GeneralConfig(APIView):
    """ serves general configuration """

    swagger_schema = None

    def get(self, request, **kwargs):
        config = {
            "enable_aquifers_search": get_env_variable("ENABLE_AQUIFERS_SEARCH") == "True",
            "sso_idp_hint": get_env_variable("SSO_IDP_HINT", "idir")
        }
        return Response(config)


class AnalyticsConfig(APIView):
    """ serves analytics config """

    def get(self, request, **kwargs):
        config = {
            "enable_google_analytics": get_env_variable("ENABLE_GOOGLE_ANALYTICS") == "True"
        }
        return Response(config)


class InsideBC(APIView):
    """ Check if a given point is inside BC """

    def get(self, request, **kwargs):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        return Response({
            'inside': isPointInsideBC(latitude, longitude)
        })


@csrf_exempt
def api_404(request, **kwargs):
    response = JsonResponse({
        'detail': 'API endpoint not found "{}"'.format(request.path)
    }, status=404)
    return response
