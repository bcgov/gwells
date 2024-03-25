from django.contrib.gis.geos import GEOSGeometry
from gwells.models import Border
import json 
import requests
from requests.exceptions import HTTPError


def isPointInsideBC(latitude, longitude):
    """
    Tests latitude and longitude to see if it falls within BC
    """

    if latitude and longitude:
        latitude = float(latitude)
        longitude = float(longitude)
        wgs84_srid = 4269
        pnt = GEOSGeometry('POINT({} {})'.format(longitude, latitude), srid=wgs84_srid)
        result = Border.objects.filter(geom__contains=pnt)
        return result.count() > 0
    return False


def setup_parameters(options):
    default_options = {
        "provinceCode": "BC",
        "outputSRS": 4326,
        "maxResults": 1,
        "minScore": 65
    }
    return {**default_options, **options}

def perform_api_request(url, params):
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp
    except requests.HTTPError as e:
        raise e

def process_response(response):
    try:
        features = response.json().get('features')
        if not features:
            raise ValueError("Unable to geocode address")
        return features[0]
    except AttributeError:
        raise ValueError("Unable to geocode address")

def geocode_bc_location(options={}):
    """
    Performs an HTTP request to the BC Physical Address Geocoder API, 
    returning a django.contrib.gis.geos.Point for the first result. Supports query 
    string parameters via the 'options' argument. Raises HTTPError for 
    communication issues and ValueError if no matching coordinate is found.
    Example 'options': {"addressString": "101 main st.", "localityName": "Kelowna"}.
    """
    params = setup_parameters(options)
    url = "https://geocoder.api.gov.bc.ca/addresses.json"
    response = perform_api_request(url, params)
    first_feature = process_response(response)

    try:
        point = GEOSGeometry(json.dumps(first_feature.get("geometry", {})))
    except TypeError:
        raise ValueError("Unable to geocode address")
    
    return point