from rest_framework.response import Response
from rest_framework.views import APIView

from gwells.settings.base import get_env_variable
from django.contrib.gis.geos import GEOSGeometry
from gwells.models import Border


class KeycloakConfig(APIView):
    """ serves keycloak config """

    def get(self, request):
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

    def get(self, request):
        config = {
            "enable_aquifers_search": get_env_variable("ENABLE_AQUIFERS_SEARCH") == "True",
            "sso_idp_hint": get_env_variable("SSO_IDP_HINT", "idir")
        }
        return Response(config)


class AnalyticsConfig(APIView):
    """ serves analytics config """

    def get(self, request):
        config = {
            "enable_google_analytics": get_env_variable("ENABLE_GOOGLE_ANALYTICS") == "True"
        }
        return Response(config)


class InsideBC(APIView):
    """ Check if a given point, is inside BC """

    def get(self, request):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        inside = False
        if latitude and longitude:
            latitude = float(latitude)
            longitude = float(longitude)
            wgs84_srid = 4269
            pnt = GEOSGeometry('POINT({} {})'.format(longitude, latitude), srid=wgs84_srid)
            result = Border.objects.filter(geom__contains=pnt)
            inside = result.count() > 0

        return Response({
            'inside': inside
        })
