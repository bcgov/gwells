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


def geocode_bc_address(address_string, locality_name=None, target_srid=4326, min_score=65):
    """
    Converts a BC address string into a geographic coordinate 
    with the specified srid (defaults to 4326, which lat/lon,WGS84).  
    The implementation makes an HTTP call to the BC Physical Address Geocoder API
    (https://www2.gov.bc.ca/gov/content/data/geographic-data-services/location-services/geocoder).
    If the address is successfully geocoded then this method returns a 
    django.contrib.gis.geos.Point object.  If a HTTP error occurs during 
    communication with the remote API then an HTTPError exception is 
    raised.  If the API call succeeds but does not find a coordinate 
    matching the given address_string, then a ValueError is raised.
    :param address_string: an address, such as "101 main st."
    :param locality_name: the name of the city or municipality of the address
    :param target_srid: the EPSG code identifying the spatial reference system of
    the response
    :param min_score: a number 0-100 indicating the minimum level of confidence to
    accept from the geocoder API.
    """
    url = "https://geocoder.api.gov.bc.ca/addresses.json"
    params = {
      "addressString": address_string,
      "maxResults": 1,
      "provinceCode": "BC",
      "outputSRS": target_srid,
      "minScore": min_score
    }
    if locality_name:
      params["localityName"] = locality_name
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
    except HTTPError as e:
        #caught and re-raised to be clear ane explicit which exceptions 
        #this method may cause
        raise e

    features = []
    
    try: 
        features = resp.json().get('features')
    except AttributeError as e:
        raise ValueError("Unable to geocode address")

    if not len(features):
        raise ValueError("Unable to geocode address")
    
    first_feature = features[0]
    try:
        point = GEOSGeometry(json.dumps(first_feature.get("geometry", {})))
    except TypeError as e:
        raise ValueError("Unable to geocode address")
    
    return point