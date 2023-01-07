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

from django.contrib.gis.geos import GEOSGeometry, GEOSException
from django.contrib.gis.db.models.functions import Transform
from rest_framework.exceptions import ValidationError
from rest_framework.filters import BaseFilterBackend

class GeometryFilterBackend(BaseFilterBackend):
    """
    Filter that allows geographic filtering on a geometry/shape using `?within=<geojson geometry>`
    """

    def filter_queryset(self, request, queryset, view):
        within = request.query_params.get('within', None)
        srid = request.query_params.get('srid', 4326)

        if within:
            try:
                shape = GEOSGeometry(within, srid=int(srid))
            except (ValueError, GEOSException):
                raise ValidationError({
                    'within': 'Invalid geometry. Use a geojson geometry or WKT representing a polygon. Example: &within={"type": "Polygon", "coordinates": [...]}'
                })
            else:
                queryset = queryset.filter(registrations__organization__geom__intersects=shape)
                
        return queryset
