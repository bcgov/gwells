from django.contrib.gis.geos import GEOSGeometry

from gwells.models import Border


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
