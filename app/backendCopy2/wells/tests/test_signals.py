from django.test import TestCase
from django.contrib.gis.geos import Point
from wells.models import Well
from wells.signals import update_utm

class TestSignals(TestCase):
    def test_update_utm__no_geom__well_not_updated(self):
        well = Well(geom=None)

        update_utm(sender=None, instance=well)

        self.assertEqual(well.utm_zone_code, None)
        self.assertEqual(well.utm_easting, None)
        self.assertEqual(well.utm_northing, None)

    def test_update_utm__geom_longitude_below_valid_range__well_not_updated(self):
        well = Well(geom="POINT(-181.00 49.26)")

        update_utm(sender=None, instance=well)

        self.assertEqual(well.utm_zone_code, None)
        self.assertEqual(well.utm_easting, None)
        self.assertEqual(well.utm_northing, None)

    def test_update_utm__geom_longitude_above_valid_range__well_not_updated(self):
        well = Well(geom="POINT(181.00 49.26)")

        update_utm(sender=None, instance=well)

        self.assertEqual(well.utm_zone_code, None)
        self.assertEqual(well.utm_easting, None)
        self.assertEqual(well.utm_northing, None)

    def test_update_utm__geom_valid__well_updated(self):
        well = Well(geom="POINT(-122.540000 49.260000)")

        update_utm(sender=None, instance=well)

        self.assertEqual(well.utm_zone_code, 10)
        self.assertEqual(well.utm_easting, 533470)
        self.assertEqual(well.utm_northing, 5456461)
