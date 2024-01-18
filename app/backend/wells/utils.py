import requests
import geopandas as gpd
from time import sleep
from shapely.geometry import Point
from wells.constants import ADDRESS_COLUMNS, GEOCODER_ENDPOINT
from thefuzz import fuzz
from django.db.models import Case, When, Value, DateField, F
from wells.models import Well

WELL_STATUS_CODE_CONSTRUCTION = 'CONSTRUCTION'
WELL_STATUS_CODE_ALTERATION = 'ALTERATION'
WELL_STATUS_CODE_DECOMMISSION = 'DECOMMISSION'

def calculate_pid_distance_for_well(well):
    """
    Calculate the distance from a single well to the nearest parcel using a WFS query.
    :param well: A well instance with latitude, longitude attributes
    :return: Distance to the nearest parcel
    """
    # Base URL for the WFS request
    base_url = "https://openmaps.gov.bc.ca/geo/pub/wfs"
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeName": "WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW",
        "outputFormat": "json",
        "srsName": "EPSG:4326",
        "CQL_FILTER": f"DWITHIN(geometry, POINT({well.longitude} {well.latitude}), 0.1, meters)"
    }

    # Construct the request URL
    request_url = f"{base_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

    # Make the request
    response = requests.get(request_url)
    if response.status_code != 200:
        print("Error making request to WFS service.")
        return None

    # Load response into GeoDataFrame
    data = response.json()
    parcels_gdf = gpd.GeoDataFrame.from_features(data["features"])

    if parcels_gdf.empty:
        print("No parcels found near well location.")
        return None

    # Calculate the distance from the well to the nearest parcel
    well_point = Point(well.longitude, well.latitude)
    parcels_gdf["distance"] = parcels_gdf.distance(well_point)

    return parcels_gdf["distance"].min()


def calculate_natural_resource_region_for_well(well):
    """
    Retrieve the natural resource region name that a well is within using a WFS query.
    :param well: A well instance with latitude, longitude attributes
    :return: Natural Resource Region name
    """
    # Base URL for the WFS request
    base_url = "https://openmaps.gov.bc.ca/geo/pub/wfs"
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeName": "WHSE_ADMIN_BOUNDARIES.ADM_NR_REGIONS_SPG",
        "outputFormat": "json",
        "srsName": "EPSG:4326",
        "CQL_FILTER": f"CONTAINS(SHAPE, POINT({well.longitude} {well.latitude}))"
    }

    # Construct the request URL
    request_url = f"{base_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

    # Make the request
    response = requests.get(request_url)
    if response.status_code != 200:
        print("Error making request to WFS service.")
        return None

    # Load response into GeoDataFrame
    data = response.json()
    regions_gdf = gpd.GeoDataFrame.from_features(data["features"])

    if regions_gdf.empty:
        print("No natural resource regions found near well location.")
        return None

    # Assuming the well can only be in one region, return the name of the first region found
    return regions_gdf.iloc[0]['properties']['REGION_ORG_UNIT_NAME']


def reverse_geocode(
    x,
    y,
    distance_start=200,
    distance_increment=200,
    distance_max=2000,
):
    """
    Provided a location as x/y coordinates (EPSG:4326), request an address
    from BC Geocoder within given distance_start (metres)

    If no result is found, request using an expanding search radius in
    distance_increment steps, until distance_max is reached.

    A dict with 'distance' = 99999 is returned if no result is found.

    """
    result = False
    distance = distance_start
    # expand the search distance until we get a result or hit the max distance
    while result is False and distance <= distance_max:
        params = {
            "point": str(x) + "," + str(y),
            "apikey": 'fake_api_key', # api key not required to be valid
            "outputFormat": "json",
            "maxDistance": distance,
        }
        r = requests.get(GEOCODER_ENDPOINT, params=params)

        # pause for 2s per request if near limit of 1000 requests/min
        if int(r.headers["RateLimit-Remaining"]) < 30:
            sleep(2)
        if r.status_code == 200:
            result = True
        else:
            distance = distance + distance_increment
    if r.status_code == 200:
        address = r.json()["properties"]
        address["distance"] = distance
        return address
    else:
        empty_result = dict([(k, "") for k in ADDRESS_COLUMNS])
        empty_result["distance"] = 99999
        return empty_result


def calculate_geocode_distance(geocoded_address):
    if not geocoded_address:
        return None
    return geocoded_address.get('distance', None)


def calculate_score_address(well, geocoded_address):
    if not geocoded_address:
        return None
    return fuzz.token_set_ratio(well.street_address.lower(), geocoded_address.get('fullAddress', '').lower())


def calculate_score_city(well, geocoded_address):
    if not geocoded_address:
        return None
    return fuzz.token_set_ratio(well.city.lower(), geocoded_address.get('localityName', '').lower())


def get_annotated_well_queryset():
    return Well.objects.select_related('well_status').annotate(
        work_start_date=Case(
            When(well_status__well_status_code=WELL_STATUS_CODE_CONSTRUCTION, then=F('construction_start_date')),
            When(well_status__well_status_code=WELL_STATUS_CODE_ALTERATION, then=F('alteration_start_date')),
            When(well_status__well_status_code=WELL_STATUS_CODE_DECOMMISSION, then=F('decommission_start_date')),
            default=Value(None),
            output_field=DateField()
        ),
        work_end_date=Case(
            When(well_status__well_status_code=WELL_STATUS_CODE_CONSTRUCTION, then=F('construction_end_date')),
            When(well_status__well_status_code=WELL_STATUS_CODE_ALTERATION, then=F('alteration_end_date')),
            When(well_status__well_status_code=WELL_STATUS_CODE_DECOMMISSION, then=F('decommission_end_date')),
            default=Value(None),
            output_field=DateField()
        )
    )