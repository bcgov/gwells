import math
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from wells.models import Well
from wells.utils import calculate_geocode_distance, calculate_pid_distance_for_well, \
  calculate_score_address, calculate_score_city, calculate_natural_resource_region_for_well, \
  reverse_geocode

@receiver(pre_save, sender=Well)
def update_utm(sender, instance, **kwargs):
    if instance.geom and (-180 < instance.geom.x < 180): # only update utm when geom is valid
        utm_zone = math.floor((instance.geom.x + 180) / 6) + 1
        coord_transform = CoordTransform(SpatialReference(4326), SpatialReference(32600 + utm_zone))
        utm_point = instance.geom.transform(coord_transform, clone=True)

        instance.utm_zone_code = utm_zone
        # We round to integers because easting/northing is only precise to 1m. The DB column is also an integer type.
        instance.utm_easting = round(utm_point.x)
        instance.utm_northing = round(utm_point.y)


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

    try:
        if instance._state.adding and not instance.pk:
            # Handling new instance creation
            if is_valid_geom(instance.geom):
                set_well_attributes(instance)
        else:
            # Handling updates to existing instances
            original_instance = sender.objects.get(pk=instance.pk)
            if original_instance.geom != instance.geom and is_valid_geom(instance.geom):
                set_well_attributes(instance)
    except Exception as e:
        print(f"Error in update_well for Well ID {instance.pk}: {str(e)}")


def set_well_attributes(instance):
    """
    Set attributes for a Well instance based on its geographical location.

    Parameters:
    instance (Well instance): The instance of Well being processed.
    """
    geocoded_address = reverse_geocode(instance.longitude, instance.latitude)
    instance.geocode_distance = calculate_geocode_distance(geocoded_address)
    instance.distance_to_pid = calculate_pid_distance_for_well(instance)
    instance.score_address = calculate_score_address(instance, geocoded_address)
    instance.score_city = calculate_score_city(instance, geocoded_address)
    instance.natural_resource_region = calculate_natural_resource_region_for_well(instance)