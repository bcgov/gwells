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

from aquifers.models import Aquifer

class AquiferSerializer(serializers.ModelSerializer):
    """Serialize a aquifer list"""
    demand_description = serializers.SlugRelatedField(source='demand', read_only=True, slug_field='description')
    material_description = serializers.SlugRelatedField(source='material', read_only=True, slug_field='description')
    productivity_description = serializers.SlugRelatedField(source='productivity', read_only=True, slug_field='description')
    subtype_description = serializers.SlugRelatedField(source='subtype', read_only=True, slug_field='description')
    vulnerability_description = serializers.SlugRelatedField(source='vulnerability', read_only=True, slug_field='description')
    quality_concern_description = serializers.SlugRelatedField(source='quality_concern', read_only=True, slug_field='description')

    class Meta:
        model = Aquifer
        fields = (
            'aquifer_id',
            'aquifer_name',
            'area',
            'demand_description',
            'demand',
            'litho_stratographic_unit',
            'location_description',
            'mapping_year',
            'material_description',
            'material',
            'productivity_description',
            'productivity',
            'quality_concern_description',
            'quality_concern',
            'subtype_description',
            'subtype',
            'vulnerability_description',
            'vulnerability'
        )