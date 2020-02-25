"""
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
import logging
from decimal import Decimal

from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry, Point

from gwells.utils import isPointInsideBC
from wells.models import Well
from aquifers.models.vertical_aquifer_extents import VerticalAquiferExtent


logger = logging.getLogger(__name__)


class WellLocationSerializerV2(serializers.ModelSerializer):
    """ serializes well locations """

    class Meta:
        model = Well
        fields = ("well_tag_number", "identification_plate_number",
                  "latitude", "longitude", "street_address", "city", "ems")


class WellVerticalAquiferExtentSerializerV2(serializers.ModelSerializer):
    # start = serializers.DecimalField(max_digits=7, decimal_places=2, required=True, allow_null=False)
    aquifer_id = serializers.IntegerField()
    aquifer_name = serializers.CharField(source='aquifer.aquifer_name', read_only=True)
    well_tag_number = serializers.IntegerField(write_only=True)

    class Meta:
        model = VerticalAquiferExtent
        fields = (
            'id',
            'aquifer_id',
            'aquifer_name',
            'well_tag_number',
            'start',
            'end',
            'geom'
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.geom:
            ret['lat'] = Decimal(instance.geom.y)
            ret['lng'] = Decimal(instance.geom.x)
        del ret['geom']
        return ret

    def to_internal_value(self, data):
        latitude = data.pop('lat', None)
        longitude = data.pop('lng', None)
        well_tag_number = data.get('well_tag_number', None)

        errors = {}
        # If lat and lng are not in the payload then we want to use the well's lat lng
        if latitude is None and longitude is None and well_tag_number:
            well = Well.objects.get(well_tag_number=well_tag_number)
            if well.geom:
                longitude = well.geom.x
                latitude = well.geom.y

        if latitude == '' or latitude is None:
            errors['lat'] = ['This field is required.']
        if longitude == '' or longitude is None:
            errors['lng'] = ['This field is required.']

        if len(errors) > 0:
            raise serializers.ValidationError(errors)

        point = Point(-abs(float(longitude)), float(latitude), srid=4326)

        data['geom'] = point
        return super(WellVerticalAquiferExtentSerializerV2, self).to_internal_value(data)

    def validate(self, attrs):
        errors = {}

        start_depth = attrs.get('start', None)
        end_depth = attrs.get('end', None)
        if start_depth is not None and end_depth is not None:
            if start_depth > end_depth:
                errors['end'] = 'To can not be above from'
            if abs(end_depth - start_depth) < Decimal('0.1'):
                errors['end'] = 'End must be more then 0.1m from start'

        point = attrs.get('geom')
        if point:
            isInside = isPointInsideBC(point.y, point.x)
            if not isInside:
                errors['lat'] = 'Latitude is not inside BC'
                errors['lng'] = 'Longitude is not inside BC'

        if len(errors) > 0:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        well_tag_number = validated_data.pop('well_tag_number', None)
        well = Well.objects.get(well_tag_number=well_tag_number)
        validated_data['well'] = well
        return super().create(validated_data)
