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

from rest_framework import serializers

from aquifers import models


class AquiferResourceSerializer(serializers.ModelSerializer):
    """Serialize aquifer resourcelist"""
    section_id = serializers.PrimaryKeyRelatedField(
        queryset=models.AquiferResourceSection.objects.all(),
        source='section.id')

    def to_internal_value(self, data):
        """
        Dict of native values <- Dict of primitive datatypes.
        Add instance key to values if `id` present in primitive dict
        :param data:
        """
        obj = super(AquiferResourceSerializer, self).to_internal_value(data)
        instance_id = data.get('id', None)
        if instance_id:
            obj['instance'] = models.AquiferResource.objects.get(id=instance_id)
        return obj

    class Meta:
        model = models.AquiferResource
        fields = (
            'id',
            'name',
            'url',
            'section_id'
        )


class AquiferSerializer(serializers.ModelSerializer):
    """Serialize a aquifer list"""
    demand_description = serializers.SlugRelatedField(
        source='demand', read_only=True, slug_field='description')
    material_description = serializers.SlugRelatedField(
        source='material', read_only=True, slug_field='description')
    productivity_description = serializers.SlugRelatedField(
        source='productivity', read_only=True, slug_field='description')
    subtype_description = serializers.StringRelatedField(
        source='subtype', read_only=True)
    vulnerability_description = serializers.SlugRelatedField(
        source='vulnerability', read_only=True, slug_field='description')
    quality_concern_description = serializers.SlugRelatedField(
        source='quality_concern', read_only=True, slug_field='description')
    known_water_use_description = serializers.SlugRelatedField(
        source='known_water_use', read_only=True, slug_field='description')
    resources = AquiferResourceSerializer(many=True)
    
    def create(self, validated_data):
        """
        Allow creating resources inline of the aquifer API. ie)

        {
            resources: [{

            }, {

            }]
        }
        """
        resources_data = validated_data.pop('resources')
        aquifer = models.Aquifer.objects.create(**validated_data)
        for resource_item in resources_data:
            models.AquiferResource.objects.create(aquifer=aquifer, **resource_item)
        return aquifer
    
    def update(self, instance, validated_data):
        """
        Update the resources associated with an aquifer, inline of the aquifer API.
        """
        resources_data = validated_data.pop('resources')
        for k,v in validated_data.items():
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
                resource.section = resource_item['section']['id']
                resource.name = resource_item['name']
                resource.url = resource_item['url']
                resource.save()
            else:
                r = models.AquiferResource(
                    url=resource_item['url'],
                    name=resource_item['name'],
                    aquifer=instance,
                    section_id=resource_item['section']['id'].id)
                r.save()

        return instance
    
    class Meta:
        model = models.Aquifer
        fields = (
            'aquifer_id',
            'aquifer_name',
            'area',
            'demand_description',
            'demand',
            'known_water_use_description',
            'known_water_use',
            'litho_stratographic_unit',
            'location_description',
            'mapping_year',
            'material_description',
            'material',
            'notes',
            'productivity_description',
            'productivity',
            'quality_concern_description',
            'quality_concern',
            'subtype_description',
            'subtype',
            'vulnerability_description',
            'vulnerability',
            'resources',
        )


class AquiferResourceSectionSerializer(serializers.ModelSerializer):
    """Serialize aquifer section list"""
    class Meta:
        model = models.AquiferResourceSection
        fields = (
            'id',
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
