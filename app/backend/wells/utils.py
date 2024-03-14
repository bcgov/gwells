import json
import requests
import geopandas as gpd
from time import sleep
from shapely.geometry import Point
from django.contrib.gis.geos import GEOSGeometry
from wells.constants import ADDRESS_COLUMNS, GEOCODER_ENDPOINT
from thefuzz import fuzz
from django.db.models import Case, When, Value, DateField, F
from wells.models import Well
from pyproj import Proj, transform

WELL_STATUS_CODE_CONSTRUCTION = 'CONSTRUCTION'
WELL_STATUS_CODE_ALTERATION = 'ALTERATION'
WELL_STATUS_CODE_DECOMMISSION = 'DECOMMISSION'
EPSG_4326 = 'epsg:4326'
EPSG_3005 = 'epsg:3005'

def calculate_pid_distance_for_well(well):
    """
    Calculate the distance from a single well to the nearest parcel using a WFS query.
    :param well: A well instance with latitude, longitude attributes
    :return: Distance to the nearest parcel in meters
    """
    # Define projections
    proj_4326 = Proj(init=EPSG_4326)  # WGS 84
    proj_3005 = Proj(init=EPSG_3005)  # NAD83 / BC Albers, uses meters

    # Transform the well's point to NAD83 / BC Albers
    x_3005, y_3005 = transform(proj_4326, proj_3005, well.longitude, well.latitude)
    well_point_3005 = Point(x_3005, y_3005)

    # Define base URL and parameters for the WFS request
    base_url = "https://openmaps.gov.bc.ca/geo/pub/wfs"
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeName": "WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW",
        "outputFormat": "json",
        "srsName": "EPSG:3005",  # Ensure the response is in the same projection as the well point
        "CQL_FILTER": f"PID_NUMBER={well.legal_pid}"
    }

    # Construct and make the request
    response = requests.get(f"{base_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}")
    if response.status_code != 200:
        print("Error making request to WFS service.")
        return None

    # Load response into GeoDataFrame, already in EPSG:3005
    data = response.json()
    parcels_gdf = gpd.GeoDataFrame.from_features(data["features"], crs="EPSG:3005")

    if parcels_gdf.empty:
        print("No parcels found for the specified PID.")
        return None

    # Calculate distances in meters from the well to each parcel
    parcels_gdf["distance"] = parcels_gdf.geometry.distance(well_point_3005)

    # Return the minimum distance
    min_distance = parcels_gdf["distance"].min()

    return round(min_distance)


def calculate_natural_resource_region_for_well(well):
    """
    Retrieve the natural resource region name that a well is within using a WFS query.
    :param well: A well instance with latitude, longitude attributes
    :return: Natural Resource Region name
    """
    # convert between projections
    proj_4326 = Proj(init=EPSG_4326)  # WGS 84
    proj_3005 = Proj(init=EPSG_3005)  # NAD83 / BC Albers

    # Transform the point
    x_3005, y_3005 = transform(proj_4326, proj_3005, well.longitude, well.latitude)

    # Base URL for the WFS request
    base_url = "https://openmaps.gov.bc.ca/geo/pub/wfs"
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeName": "WHSE_ADMIN_BOUNDARIES.ADM_NR_REGIONS_SPG",
        "outputFormat": "json",
        "srsName": "EPSG:4326",
        "CQL_FILTER": f"CONTAINS(SHAPE, POINT({x_3005} {y_3005}))",
        "propertyName": "REGION_NAME,ORG_UNIT_NAME"
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
    return regions_gdf.iloc[0]['ORG_UNIT_NAME']


def geocode(options={}):
    """
    Performs an HTTP request to the BC Physical Address Geocoder API, 
    returning a django.contrib.gis.geos.Point for the first result. Supports query 
    string parameters via the 'options' argument. Raises HTTPError for 
    communication issues and ValueError if no matching coordinate is found.
    Example 'options': {"addressString": "101 main st.", "localityName": "Kelowna"}.
    """
    url = "https://geocoder.api.gov.bc.ca/addresses.json"
    try:
        response = requests.get(url, params=options)
        
        # Check if response status is ok
        if response.status_code == 200:
            data = response.json()
            first_feature = data.get("features", [])[0] if data.get("features") else None

            if first_feature:
                geometry = first_feature.get("geometry", {})
                # Directly extract coordinates to create a shapely Point
                coordinates = geometry.get("coordinates", [])
                if coordinates:
                    # Note the order: GeoJSON specifies coordinates as [longitude, latitude]
                    shapely_point = Point(coordinates[0], coordinates[1])
                    return shapely_point
                else:
                    raise ValueError("Geometry coordinates not found.")
            else:
                raise ValueError("No matching coordinate found for the given address.")
        else:
            response.raise_for_status()  # This will raise an HTTPError if the response was an error
    except Exception as e:
        print(f"Error during geocoding: {e}")
        return None


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
    try:
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
            address = r.json().get("properties", {})
            if address:  # Check if address is not empty
                address["distance"] = distance
                return address
        # If no address return we default to an empty result
        empty_result = dict([(k, "") for k in ADDRESS_COLUMNS])
        empty_result["distance"] = 99999
        return empty_result
    except Exception as e:
        print("geocode error:", e)


def calculate_geocode_distance(well):
    """
    Calculates the geodesic distance between a well's location and its geocoded address.

    :param well: An object that contains the well's address, city, longitude, and latitude.
    :return: The distance in meters between the well's actual location and its geocoded address.
    """
    # Prepare the geocode request options with the well's street address and city
    options = {"addressString": well.street_address or '', "localityName": well.city or ''}

    # Check if both addressString and localityName are empty, return None if true
    if not options["addressString"].strip() and not options["localityName"].strip():
        print("Both addressString and localityName are empty. Skipping geocode.")
        return None

    # Geocode the address to get a point representation (assuming WKT format)
    geocoded_point = geocode(options)
    well_point = Point(well.longitude, well.latitude)

    # Initialize projections for WGS84 and UTM Zone 10N (example)
    proj_wgs84 = Proj(init='EPSG:4326')
    proj_utm = Proj(init='epsg:32610')
    # Transform the geocoded point and the well's location from WGS84 to UTM coordinates
    x1, y1 = transform(proj_wgs84, proj_utm, geocoded_point.x, geocoded_point.y)
    x2, y2 = transform(proj_wgs84, proj_utm, well_point.x, well_point.y)
    # Calculate the distance between the points in meters within the UTM projection
    distance_meters = Point(x1, y1).distance(Point(x2, y2))

    return round(distance_meters)


def calculate_score_address(well, geocoded_address):
    """
    Calculates the similarity score between the well's address and the geocoded address.

    :param well: An object that contains the well's street address.
    :param geocoded_address: A dictionary containing the full address as geocoded.
    :return: A similarity score or None if geocoded_address is not provided.
    """
    if not geocoded_address:
        # Return None if there's no geocoded address to compare with
        return None
    # Ensure the well's address is lowercased, using an empty string if address is None
    street_address_lower = well.street_address.lower() if well.street_address is not None else ''
    # Safely get the lowercased full address from geocoded_address, default to an empty string
    geocoded_address_lower = geocoded_address.get('fullAddress', '').lower()
    # Calculate and return the fuzzy similarity score between the two addresses
    return fuzz.token_set_ratio(street_address_lower, geocoded_address_lower)


def calculate_score_city(well, geocoded_address):
    """
    Calculates the similarity score between the well's city and the geocoded city.

    :param well: An object that contains the well's city.
    :param geocoded_address: A dictionary containing the city name as 'localityName'.
    :return: A similarity score or None if geocoded_address is not provided.
    """
    if not geocoded_address:
        # Return None if there's no geocoded address to compare with
        return None
    # Ensure the well's city is lowercased, using an empty string if city is None
    city_lower = well.city.lower() if well.city is not None else ''
    # Safely get the lowercased locality name from geocoded_address, default to an empty string
    locality_name_lower = geocoded_address.get('localityName', '').lower()
    # Calculate and return the fuzzy similarity score between the two city names
    return fuzz.token_set_ratio(city_lower, locality_name_lower)