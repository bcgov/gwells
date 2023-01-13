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


def geocode_bc_location(options={}):
    """
    Makes an HTTP call to the BC Physical Address Geocoder API
    (https://www2.gov.bc.ca/gov/content/data/geographic-data-services/location-services/geocoder)
    using any options provided as query string parameters. (the 'options'
    parameter supports any query string parameter supported by the "addresses.json" 
    endpoint.
    If the address is successfully geocoded then this method returns a 
    django.contrib.gis.geos.Point object corresponding to the first result.  
    If a HTTP error occurs during 
    communication with the remote API then an HTTPError exception is 
    raised.  If the API call succeeds but does not find a coordinate 
    matching the given address_string, then a ValueError is raised.
    :param options: typical options are:
      {
        "addressString": "101 main st.",
        "localityName": "Kelowna"
      }
    """
    default_options = {
      "provinceCode": "BC",
      "outputSRS": 4326,
      "maxResults": 1,
      "minScore": 65
    }
    params = {}
    params.update(default_options)
    params.update(options)

    url = "https://geocoder.api.gov.bc.ca/addresses.json"
        
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