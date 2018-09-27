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

class AquiferListSerializer(serializers.ModelSerializer):
    """Serialize a aquifer list"""

    class Meta:
        model = Aquifer
        fields = (
            'aquifer_id',
            'aquifer_name',
            'location_description',
            'material',
            'litho_stratographic_unit',
            'subtype',
            'area',
            'productivity',
            'demand',
            'mapping_year'
        )