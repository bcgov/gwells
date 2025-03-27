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
import json

from rest_framework import serializers
from django.db.models import Max
from django.contrib.gis.geos import GEOSGeometry

from aquifers import models

HYDRAULIC_SUBTYPES = ['1a', '1b', '1c', '2', '3', '4a', '5']


class AquiferResourceSerializerV2(serializers.ModelSerializer):
    """Serialize aquifer resourcelist"""
    section_code = serializers.PrimaryKeyRelatedField(
        queryset=models.AquiferResourceSection.objects.all(),
        source='section.code')

    def to_internal_value(self, data):
        """
        Dict of native values <- Dict of primitive datatypes.
        Add instance key to values if `id` present in primitive dict
        :param data:
        """
        obj = super(AquiferResourceSerializerV2, self).to_internal_value(data)
        instance_id = data.get('id', None)
        if instance_id:
            obj['instance'] = models.AquiferResource.objects.get(
                id=instance_id)
        return obj

    class Meta:
        model = models.AquiferResource
        fields = (
            'id',
            'name',
            'url',
            'section_code'
        )


class AquiferSerializerV2(serializers.ModelSerializer):
    """Serialize an aquifer list"""
    extent = serializers.SerializerMethodField()

    def get_extent(self, obj):
        """
        Gets a GeoJSON extent
        """
        extent_raw_geom = obj["extent"]
        if extent_raw_geom is not None:
            extent_geometry = GEOSGeometry(extent_raw_geom)
            return extent_geometry.extent
        return None

    def to_representation(self, instance):
        """
        Rather the declare serializer fields, we must reference them here because
        they are queried as a `dict`, which dramatically improves performance
        due to the high number of joined tables needing pruned in the associated query.

        Note: we also use short field names to save 100 kB over the network, since there are over 1000 records
        routinely fetched
        """
        ret = super().to_representation(instance)
        ret['id'] = instance['aquifer_id']
        ret['name'] = instance['aquifer_name']
        if instance['area']:
            ret['area'] = float(instance.get('area'))
        ret['lsu'] = instance['litho_stratographic_unit']

        ret['location'] = instance['location_description']

        ret['demand'] = instance['demand__description']
        ret['material'] = instance['material__description']
        ret['subtype'] = instance['subtype__description']
        ret['vulnerability'] = instance['vulnerability__description']
        ret['productivity'] = instance['productivity__description']
        return ret

    class Meta:
        model = models.Aquifer
        fields = (
            'aquifer_id',
            'mapping_year',
            'extent',
            'retire_date'
        )


class AquiferEditDetailSerializerV2(serializers.ModelSerializer):
    """
    Read serializer for aquifer details with primary key references needed for populating an edit form
    """

    resources = AquiferResourceSerializerV2(many=True, required=False)
    licence_details = serializers.JSONField(read_only=True)

    class Meta:
        model = models.Aquifer
        fields = (
            'aquifer_id',
            'aquifer_name',
            'location_description',

            'quality_concern',
            'material',
            'subtype',
            'vulnerability',
            'known_water_use',
            'litho_stratographic_unit',
            'productivity',

            'demand',
            'mapping_year',
            'resources',
            'area',
            'notes',
            'licence_details',

            'effective_date',
            'expiry_date',
            'retire_date',
        )


class AquiferDetailSerializerV2(serializers.ModelSerializer):

    resources = AquiferResourceSerializerV2(many=True, required=False)
    licence_details = serializers.JSONField(read_only=True)

    def create(self, validated_data):
        """
        Allow creating resources inline of the aquifer API. ie)

        {
            resources: [{
                url: 'http://...',
                name: 'A resource',
                section_id: 1
            }, {
                ...
            }, ...]
            ...
        }
        """
        resources_data = validated_data.pop('resources', [])
        aquifer = models.Aquifer.objects.create(**validated_data)
        for resource_item in resources_data:
            aquifer_resource = models.AquiferResource(
                url=resource_item['url'],
                name=resource_item['name'],
                aquifer=aquifer,
                section_id=resource_item['section']['code'].code)
            aquifer_resource.save()
        return aquifer

    def update(self, instance, validated_data):
        """
        Update the resources associated with an aquifer, inline of the aquifer API.
        """
        resources_data = validated_data.pop('resources', [])
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        # Any items removed from the inline collection are deleted.
        to_delete = models.AquiferResource.objects.filter(
            aquifer=instance
        ).exclude(
            id__in=[r['id'] for r in resources_data if 'id' in r]
        )

        to_delete.delete()

        for resource_item in resources_data:
            if 'instance' in resource_item:
                resource = resource_item['instance']
                resource.section = resource_item['section']['code']
                resource.name = resource_item['name']
                resource.url = resource_item['url']
                resource.save()
            else:
                r = models.AquiferResource(
                    url=resource_item['url'],
                    name=resource_item['name'],
                    aquifer=instance,
                    section_id=resource_item['section']['code'].code)
                r.save()

        return instance

    def to_representation(self, instance):
        """
        Fetch many details related to a aquifer, used to generate its' summary page.
        """

        ret = super().to_representation(instance)
        if instance.geom:
            instance.geom.transform(4326)
            ret['geom'] = json.loads(instance.geom.json)

        # respond with the 'description' field for the following items, which are otherwise
        # references to code tables. Testing for the reference first prevents type errors,
        # since these fields are nullable.  If the field is null, we set these values to None
        ret['demand'] = instance.demand and instance.demand.description or None
        ret['material'] = instance.material and instance.material.description or None
        ret['productivity'] = instance.productivity and instance.productivity.description or None
        ret['subtype'] = instance.subtype and instance.subtype.description or None
        ret['vulnerability'] = instance.vulnerability and instance.vulnerability.description or None
        ret['quality_concern'] = instance.quality_concern and instance.quality_concern.description or None

        details = {}

        licences = models.WaterRightsLicence.objects.filter(
            well__aquifer=instance
        ).select_related('purpose')

        # distinct licence numbers.
        details['licence_count'] = len(
            licences.values('licence_number').distinct())

        # latest date when licence data were updated.
        details['licences_updated'] = licences.aggregate(
            Max('update_date')
        )

        # Water quality info
        details['num_wells_with_ems'] = instance.well_set.filter(
            ems__isnull=False).count()

        # Artesian conditions
        details['num_artesian_wells'] = instance.well_set.filter(
            artesian_conditions=True).count()

        # Wells associated to an aquifer
        details['wells_updated'] = instance.well_set.all().aggregate(
            Max('update_date')
        )
        details['num_wells'] = instance.well_set.all().count()
        details['obs_wells'] = instance.well_set.filter(
            observation_well_number__isnull=False
        ).values('well_tag_number', 'observation_well_number', 'observation_well_status')

        details.update(self._tally_licence_data(licences))

        if instance.subtype:
            details['hydraulically_connected'] = instance.subtype.code in HYDRAULIC_SUBTYPES

        ret['licence_details'] = details

        return ret

    def _tally_licence_data(self, licences):
        # Collect licences by number, for tallying according to logic in business area.
        # Some types of licences must be merged when calculating totals depending on
        # "quantity flags". See inline for details.
        _licence_map = {}
        for licence in licences:

            if licence.licence_number not in _licence_map:  # only insert each licence once.

                _licence_map[licence.licence_number] = {
                    'wells': [],
                    'usage_by_purpose': {}
                }

            _licence_dict = _licence_map[licence.licence_number]
            _licence_dict['wells'] = set(
                [l['well_tag_number'] for l in licence.well_set.all().values('well_tag_number')]
            ) | set(_licence_dict['wells'])

            if licence.purpose.description not in _licence_dict['usage_by_purpose']:
                _licence_dict['usage_by_purpose'][licence.purpose.description] = 0
                # for 'M' licences, only add the quantity once for the entire purpose.
                if licence.quantity_flag == 'M':
                    _licence_dict['usage_by_purpose'][licence.purpose.description] += licence.quantity

            # For any flag other than 'M' total all usage values.
            if licence.quantity_flag != 'M':
                _licence_dict['usage_by_purpose'][licence.purpose.description] += licence.quantity

        details = {
            'wells_by_licence': [],
            'usage': [],
            'lic_qty': []
        }

        # Again, generate some maps. Group by purpose this time.
        _lic_qty_map = {}
        _usage_map = {}

        # re-format well by licence output.
        for licence_number, licence_dict in _licence_map.items():
            details['wells_by_licence'].append({
                'licence_number': licence_number,
                'well_tag_numbers_in_licence': ', '.join(map(str, licence_dict['wells']))
            })
            for purpose, usage in licence_dict['usage_by_purpose'].items():
                if purpose not in _lic_qty_map:
                    _lic_qty_map[purpose] = 0
                    _usage_map[purpose] = 0
                _lic_qty_map[purpose] += 1
                _usage_map[purpose] += usage

        # re-format for final output.
        for purpose, qty in _lic_qty_map.items():
            details['lic_qty'].append({
                'purpose__description': purpose,
                'total_qty': qty
            })
            details['usage'].append({
                'purpose__description': purpose,
                'total_qty': _usage_map[purpose]
            })

        return details

    class Meta:
        model = models.Aquifer
        fields = (
            'aquifer_id',
            'aquifer_name',
            'location_description',

            'quality_concern',
            'material',
            'subtype',
            'vulnerability',
            'known_water_use',
            'litho_stratographic_unit',
            'productivity',

            'demand',
            'mapping_year',
            'resources',
            'area',
            'notes',
            'licence_details',

            'effective_date',
            'expiry_date',
            'retire_date',
        )
