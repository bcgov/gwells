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
from django.contrib.gis.geos import GEOSException, Polygon
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from rest_framework.filters import BaseFilterBackend


class BoundingBoxFilterBackend(BaseFilterBackend):
    """
    Filter that allows geographic filtering with a bounding box.
    """

    def filter_queryset(self, request, queryset, _view):
        sw_long = request.query_params.get('sw_long')
        sw_lat = request.query_params.get('sw_lat')
        ne_long = request.query_params.get('ne_long')
        ne_lat = request.query_params.get('ne_lat')

        if sw_long and sw_lat and ne_long and ne_lat:
            try:
                bbox = Polygon.from_bbox((sw_long, sw_lat, ne_long, ne_lat))
                bbox.srid = 4326
            except (ValueError, GEOSException):
                pass
            else:
                queryset = queryset.filter(geom__bboverlaps=bbox)

        return queryset
