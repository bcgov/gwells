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
from django.conf.urls import url
from django.views.decorators.cache import never_cache

from gwells.urls import app_root_slash
from . import views


urlpatterns = [

    # API endpoints

    url(r'^api/v1/wells/(?P<well_id>[0-9]+)/history$',
        never_cache(views.WellHistory.as_view()), name='well-history'),

    # Submissions for a well
    url(r'^api/v1/wells/(?P<well_id>[0-9]+)/submissions$',
        never_cache(views.WellSubmissionsListAPIView.as_view()), name='submissions-by-well'),

    # Well
    url(r'^api/v1/wells/(?P<well_tag_number>[0-9]+)$',
        never_cache(views.WellDetail.as_view()), name='well-detail'),

    # Well tag search
    url(r'^api/v1/wells/tags$',
        never_cache(views.WellTagSearchAPIView.as_view()), name='well-tag-search'),

    # Well tag search
    url(r'^api/v1/wells/locations$',
        never_cache(views.WellLocationListAPIView.as_view()), name='well-locations'),

    # Documents (well records)
    url(r'^api/v1/wells/(?P<tag>[0-9]+)/files$',
        never_cache(views.ListFiles.as_view()), name='file-list'),

    # Extract files
    url(r'^api/v1/wells/extracts$', views.ListExtracts.as_view(), name='extract-list'),

    # Document Uploading (well records)
    url(r'^api/v1/wells/(?P<tag>[0-9]+)/presigned_put_url$',
        never_cache(views.PreSignedDocumentKey.as_view()), name='well-pre-signed-url'),

    # Document Uploading (well records)
    url(r'^api/v1/wells/(?P<tag>[0-9]+)/delete_document$',
        never_cache(views.DeleteWellDocument.as_view()), name='well-delete-document'),

    # Well list
    url(r'^api/v1/wells$',
        never_cache(views.WellListAPIView.as_view()), name='well-list'),

    # GeoJSON well endpoint for DataBC.
    url(r'^api/v1/gis/wells$',
        views.well_geojson, name='well-geojson'),

    # GeoJSON lithology endpoint for DataBC.
    url(r'^api/v1/gis/lithology$',
        views.lithology_geojson, name='well-lithology-geojson')
]
