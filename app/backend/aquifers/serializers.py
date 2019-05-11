from collections import OrderedDict
from rest_framework.fields import SkipField
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
from django.db.models import Sum, Max, Count

from aquifers import models

HYDRAULIC_SUBTYPES = ['1a', '1b', '1c', '2', '3', '4a', '5']


class AquiferResourceSerializer(serializers.ModelSerializer):
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
        obj = super(AquiferResourceSerializer, self).to_internal_value(data)
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


class AquiferSerializer(serializers.ModelSerializer):
    """Serialize a aquifer list"""

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
        ret['name'] = instance['aquifer_id']
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
        )


class AquiferDetailSerializer(serializers.ModelSerializer):
    demand = serializers.SlugRelatedField(
        read_only=True, slug_field='description')
    material = serializers.SlugRelatedField(
        read_only=True, slug_field='description')
    productivity = serializers.SlugRelatedField(
        read_only=True, slug_field='description')
    subtype = serializers.StringRelatedField(
        read_only=True)
    vulnerability = serializers.SlugRelatedField(
        read_only=True, slug_field='description')
    quality_concern = serializers.SlugRelatedField(
        read_only=True, slug_field='description')
    resources = AquiferResourceSerializer(many=True, required=False)
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
            r = models.AquiferResource(
                url=resource_item['url'],
                name=resource_item['name'],
                aquifer=aquifer,
                section_id=resource_item['section']['code'].code)
            r.save()
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

        details = {}

        licences = models.WaterRightsLicence.objects.filter(
            wells__aquifer=instance
        )

        details['licence_count'] = licences.count()
        details['usage'] = licences.values(
            'purpose__description').annotate(
                total_qty=Sum('quantity')
        )
        details['lic_qty'] = licences.values(
            'purpose__description').annotate(
                total_qty=Count('quantity')
        )
        details['licences_updated'] = licences.aggregate(
            Max('update_date')
        )

        # Water quality info
        details['num_wells_with_ems'] = instance.well_set.filter(
            ems__isnull=False).count()

        # Artesian conditions
        details['num_artesian_wells'] = instance.well_set.filter(
            artesian_pressure__isnull=False,
            artesian_flow__isnull=False).count()

        # Wells associated to an aquifer
        details['wells_updated'] = instance.well_set.all().aggregate(
            Max('update_date')
        )
        details['num_wells'] = instance.well_set.all().count()
        details['obs_wells'] = instance.well_set.filter(
            observation_well_number__isnull=False
        ).values('well_tag_number', 'observation_well_number')

        details['wells_by_licence'] = []
        for licence in licences:
            details['wells_by_licence'].append({
                'licence_number': licence.licence_number,
                'wells_in_licence': ', '.join([str(l['well_tag_number']) for l in licence.wells.all().values("well_tag_number")])
            })
        if instance.subtype:
            details['hydraulically_connected'] = instance.subtype.code in HYDRAULIC_SUBTYPES

        ret['licence_details'] = details

        return ret

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
        )


class AquiferResourceSectionSerializer(serializers.ModelSerializer):
    """Serialize aquifer section list"""
    class Meta:
        model = models.AquiferResourceSection
        fields = (
            'code',
            'name'
        )


class AquiferMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AquiferMaterial
        fields = (
            'code',
            'description'
        )


class QualityConcernSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QualityConcern
        fields = (
            'code',
            'description'
        )


class AquiferVulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AquiferVulnerabilityCode
        fields = (
            'code',
            'description'
        )


class AquiferSubtypeSerializer(serializers.ModelSerializer):
    description = serializers.CharField(source='__str__')

    class Meta:
        model = models.AquiferSubtype
        fields = (
            'code',
            'description'
        )


class AquiferProductivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AquiferProductivity
        fields = (
            'code',
            'description'
        )


class AquiferDemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AquiferDemand
        fields = (
            'code',
            'description'
        )


class WaterUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WaterUse
        fields = (
            'code',
            'description'
        )


class AquiferSerializerBasic(serializers.ModelSerializer):
    """Serialize a aquifer list with a simplified format"""

    description = serializers.SerializerMethodField()

    class Meta:
        model = models.Aquifer
        fields = (
            'aquifer_id',
            'description',
        )

    def get_description(self, obj):
        desc = str(obj.aquifer_id)

        # if aquifers have a name (not all do), append it to the aquifer number
        name = obj.aquifer_name
        if name:
            desc += ' - ' + name

        return desc
