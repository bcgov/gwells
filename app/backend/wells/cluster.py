from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import GeoHash
from django.db.models import Case, CharField, Value, When


def get_precision(ne_lat, ne_long, sw_lat, sw_long):
    """ calculate 4 markers in a given bounding box """

    x = abs(sw_long - ne_long)
    y = abs(ne_lat - sw_lat)
    a = x*y

    if a > 200:
        return 2
    if a > 50:
        return 3
    if a > 10:
        return 4
    if a > 3:
        return 5
    if a > 1:
        return 6
    if a > 0.5:
        return 7
    return 8


def geohash(qs, precision):
    return qs.annotate(geom_hash=GeoHash('geom', precision))


def cluster(qs, ne_lat, ne_long, sw_lat, sw_long):
    precision = get_precision(ne_lat, ne_long, sw_lat, sw_long)
    return geohash(qs, precision).values('geom_hash').exclude(geom_hash__isnull=True).annotate(count=models.Count('geom_hash'))
