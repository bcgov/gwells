from django.test import TestCase
from django.contrib.gis.geos import Point
from wells.models import Well
from wells.signals import update_utm, _get_utm_zone, _generate_utm_point
from osgeo import ogr

class TestSignals(TestCase):
    def test_get_utm_zone(self):
        well = Well(geom=None)

        utm_zone = _get_utm_zone(well.geom)

        self.assertEqual(utm_zone, None)

    def test_get_utm_zone(self):
        well = Well(geom="POINT(-122.540000 49.260000)")

        utm_zone = _get_utm_zone(well.geom)

        self.assertEqual(utm_zone, 10)

    def test_generate_utm_point(self):
        well = Well(geom="POINT(-122.540000 49.260000)")

        utm_point = _generate_utm_point(10, well.geom)

        self.assertEqual(isinstance(utm_point, ogr.Geometry), True)
        self.assertEqual(utm_point.GetX(), 533470.030947186)
        self.assertEqual(utm_point.GetY(), 5456461.202321483)

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

    """
        I'm writing a few duplicate tests here to confirm transormation.
        I don't like using for loops in the tests.
        TODO: Ideally we can migrate to pytest and use parameterization for this in the future:
            - https://docs.pytest.org/en/7.1.x/example/parametrize.html
    """
    def test_update_utm__geom_valid__well_updated(self):
        well = Well(geom="POINT(-122.540000 49.260000)")

        update_utm(sender=None, instance=well)

        self.assertEqual(well.utm_zone_code, 10)
        self.assertEqual(well.utm_easting, 533470)
        self.assertEqual(well.utm_northing, 5456461)

    def test_update_utm__geom_valid__well_updated_2(self):
        well = Well(geom="POINT(-122.500825 49.208751)")

        update_utm(sender=None, instance=well)

        self.assertEqual(well.utm_zone_code, 10)
        self.assertEqual(well.utm_easting, 536358)
        self.assertEqual(well.utm_northing, 5450782)

    def test_update_utm__geom_valid__well_updated_3(self):
        well = Well(geom="POINT(-123.768875 48.981545)")

        update_utm(sender=None, instance=well)

        self.assertEqual(well.utm_zone_code, 10)
        self.assertEqual(well.utm_easting, 443742)
        self.assertEqual(well.utm_northing, 5425689)
