import math
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from wells.models import Well
from gwells.settings import TESTING
from wells.utils import calculate_geocode_distance, calculate_pid_distance_for_well, \
  calculate_score_address, calculate_score_city, calculate_natural_resource_region_for_well, \
  reverse_geocode

def _get_utm_zone(geom):
    if not geom:
        return
    return math.floor((geom.x + 180) / 6) + 1

def _generate_utm_point(utm_zone, geom):
    from osgeo import ogr, osr

    if utm_zone is None:
        return

    source_srs = osr.SpatialReference()
    source_srs.ImportFromEPSG(4326)

    target_srs = osr.SpatialReference()
    target_srs.ImportFromEPSG(32600 + utm_zone)

    transform = osr.CoordinateTransformation(source_srs, target_srs)

    point = ogr.Geometry(ogr.wkbPoint)

    point.AddPoint(geom.y, geom.x)

    point.Transform(transform)

    return point


@receiver(pre_save, sender=Well)
def update_utm(sender, instance, **kwargs):
    if not instance.geom:
        return
    
    geom = instance.geom
    utm_is_valid = -180 < geom.x < 180
    
    if not utm_is_valid:
        return
    
    utm_zone = _get_utm_zone(geom)

    utm_point = _generate_utm_point(utm_zone, geom)

    instance.utm_zone_code = utm_zone
    
    # We round to integers because easting/northing is only precise to 1m. The DB column is also an integer type.
    instance.utm_easting = round(utm_point.GetX())
    instance.utm_northing = round(utm_point.GetY())

if not TESTING:
    @receiver(pre_save, sender=Well)
    def update_well(sender, instance, **kwargs):
        """
        Signal receiver that triggers before a Well instance is saved.

        For new Well instances, it calculates and sets various geographical and scoring fields.
        For existing Well instances, it recalculates these fields if the geographical location (geom) has changed.

        Parameters:
        sender (Model Class): The model class that sent the signal. Should always be the Well model.
        instance (Well instance): The instance of Well being saved.
        kwargs: Additional keyword arguments. Not used in this function.
        """

        def is_valid_geom(geom):
            """
            Helper function to check if the geom attribute is valid.
            A valid geom should be non-null and must have both latitude and longitude.
            """
            return geom and hasattr(geom, 'x') and hasattr(geom, 'y')

        def contains_cross_reference_comment(comments):
            """
            Helper function to check if comments contain any of the specified search terms
            indicating a cross-reference.
            """
            search_terms = ["x-ref'd", "x-ref", "cross-ref", "cross r", "cross-r", "ref'd", "referenced", "refd", "xref", "x-r", "x r"]
            comments_lower = comments.lower() if comments is not None else ''
            return any(term in comments_lower for term in search_terms)

        try:
            if instance._state.adding and not instance.pk:
                # Handling new instance creation
                if is_valid_geom(instance.geom):
                    set_well_attributes(instance)
            else:
                # Handling updates to existing instances
                original_instance = sender.objects.get(pk=instance.pk)
                geom_changed = original_instance.geom != instance.geom
                address_changed = original_instance.street_address != instance.street_address
                city_changed = original_instance.city != instance.city
                pid_changed = original_instance.legal_pid != instance.legal_pid

                if (geom_changed or address_changed or city_changed or pid_changed) and is_valid_geom(instance.geom):
                    set_well_attributes(instance)

            # If comments indicate a cross-reference, set cross-reference attributes
            if instance.comments and contains_cross_reference_comment(instance.comments):
                set_cross_reference_attributes(instance)

        except Exception as e:
            print(f"Error in update_well for Well ID {instance.pk}: {str(e)}")


def set_cross_reference_attributes(instance):
    """
    Sets cross-reference attributes for a Well instance 
    when a user has set the comment to include one of 
    the cross referenced values.
    """
    if not instance.cross_referenced: # Only update if not already set
        instance.cross_referenced = True
        instance.cross_referenced_date = timezone.now()
        instance.cross_referenced_by = instance.update_user


def set_well_attributes(instance):
    """
    Set attributes for a Well instance based on its geographical location.

    Parameters:
    instance (Well instance): The instance of Well being processed.
    """
    # Calculate distance scores
    instance.geocode_distance = calculate_geocode_distance(instance)
    instance.distance_to_pid = calculate_pid_distance_for_well(instance)

    # Geocode point to address
    geocoded_address = reverse_geocode(instance.longitude, instance.latitude)

    # Calculate address scores
    instance.score_address = calculate_score_address(instance, geocoded_address)
    instance.score_city = calculate_score_city(instance, geocoded_address)

    # Calculate natural resource region of well
    instance.natural_resource_region = calculate_natural_resource_region_for_well(instance)