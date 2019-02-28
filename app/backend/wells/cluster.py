from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import GeoHash


def get_precision(ne_lat, ne_long, sw_lat, sw_long):
    """ calculate 4 markers in a given bounding box """

    x = sw_long - ne_long
    y = ne_lat - sw_lat

    if x > 360:
        x = 360
    if y > 180:
        y = 180

    a = x * y

    # p = ((a / 180*360) + 1) * 6

    if a < 10:
        return 7
    return 6


def geohash(qs, precision):
    return qs.annotate(geom_hash=GeoHash('geom', precision))


def cluster(qs, ne_lat, ne_long, sw_lat, sw_long):
    precision = get_precision(ne_lat, ne_long, sw_lat, sw_long)
    return geohash(qs, precision).values('geom_hash').annotate(count=models.Count('geom_hash'))
