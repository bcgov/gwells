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
    aquifer_id = serializers.PrimaryKeyRelatedField(queryset=models.Aquifer.objects.all(),source='aquifer.id')
    section_id = serializers.PrimaryKeyRelatedField(queryset=models.AquiferResourceSection.objects.all(),source='section.id')

    class Meta:
        model = models.AquiferResource
        fields = (
            'aquifer_resource_id',
            'name',
            'url'
        )


    # def create(self, validated_data):
    #     subject = Child.objects.create(
    #         aquifer=validated_data['aquifer']['id'],
    #         name=validated_data['name'],
    #         name=validated_data['url'],
    #         name=validated_data['section']['id'],
    #     )
        # return child

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
