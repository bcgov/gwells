import requests
import geojson
from geojson import Feature, FeatureCollection, Point
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from gwells.settings.base import get_env_variable
from gwells.utils import isPointInsideBC

class KeycloakConfig(APIView):
    """ Serves configuration object for Keycloak. """

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
    """ Serves general configuration object. """

    def get(self, request, **kwargs):
        config = {
            "enable_aquifers_search": get_env_variable("ENABLE_AQUIFERS_SEARCH") == "True",
            "sso_idp_hint": get_env_variable("SSO_IDP_HINT", "idir")
        }
        return Response(config)

class InsideBC(APIView):
    """ Check if a given Latitude/Longitude are inside BC """
    @swagger_auto_schema(
        manual_parameters =[
            openapi.Parameter(
                name='longitude',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_NUMBER,
                description="Longitude Coordinate"
            ),
            openapi.Parameter(
                name='latitude',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_NUMBER,
                description="Latitude Coordinate"
            )
        ]
    )
    def get(self, request, **kwargs):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        return Response({
            'inside': isPointInsideBC(latitude, longitude)
        })


class DataBCGeocoder(APIView):
    """ Looks up address using DataBC's geocoder """
    swagger_schema = None
    
    def get(self, request, **kwargs):
        query = kwargs['query']

        #default params
        params = {
            "addressString": query,
            "autoComplete": "true",
            "maxResults": 5,
            "brief": "true"
        }

        #override default params with values from request
        params.update(request.query_params.dict())

        search_url = "https://geocoder.api.gov.bc.ca/addresses.json"

        resp = requests.get(search_url, params=params)
        resp.raise_for_status()

        features = resp.json().get('features')

        geocoder_features = []

        # add metadata to features
        for feat in features:
            coordinates = feat['geometry']['coordinates']
            point = Point(coordinates)
            new_feature = Feature(geometry=point)

            # add mapbox-gl-js geocoder specific data (used for populating search box)
            new_feature['center'] = coordinates
            new_feature['place_name'] = feat.get('properties', {}).get('fullAddress')

            geocoder_features.append(new_feature)

        return HttpResponse(geojson.dumps(FeatureCollection(geocoder_features)))


@csrf_exempt
def api_404(request, **kwargs):
    response = JsonResponse({
        'detail': 'API endpoint not found "{}"'.format(request.path)
    }, status=404)
    return response
