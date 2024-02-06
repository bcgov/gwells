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
from django.views.decorators.cache import never_cache, cache_page

from . import views
from . import views_v2
from gwells.urls import api_path_prefix

CACHE_TTL = 60*15

urlpatterns = [
    url(r'api/v1/aquifers$',
        never_cache(views.AquiferListCreateAPIView.as_view()),
        name='aquifers-list-create-v1'
        ),

    url(r'api/v2/aquifers$',
        never_cache(views_v2.AquiferListCreateAPIViewV2.as_view()),
        name='aquifers-list-create-v2'
        ),

    url(r'api/v1/aquifers/csv$',
        never_cache(views.csv_export),
        name='aquifers-list-csv-v1'
        ),

    url(r'api/v2/aquifers/csv$',
        never_cache(views_v2.csv_export_v2),
        name='aquifers-list-csv-v2'
        ),

    url(r'api/v1/aquifers/xlsx$',
        never_cache(views.xlsx_export),
        name='aquifers-list-xlsx-v1'
        ),

    url(r'api/v2/aquifers/xlsx$',
        never_cache(views_v2.xlsx_export_v2),
        name='aquifers-list-xlsx-v2'
        ),

    url(r'api/v1/aquifers/names$',
        never_cache(views.AquiferNameList.as_view()),
        name='aquifer-name-list-v1'
        ),

    url(r'api/v2/aquifers/names$',
        never_cache(views_v2.AquiferNameListV2.as_view()),
        name='aquifer-name-list-v2'
        ),

    url(r'api/v1/aquifers/(?P<aquifer_id>[0-9]+)/edit$',
        never_cache(views.AquiferEditDetailsAPIViewV1.as_view()),
        name='aquifer-edit-details-v1'
        ),

    url(r'api/v2/aquifers/(?P<aquifer_id>[0-9]+)/edit$',
        never_cache(views_v2.AquiferEditDetailsAPIViewV2.as_view()),
        name='aquifer-edit-details-v2'
        ),

    url(r'api/v1/aquifers/(?P<aquifer_id>[0-9]+)$',
        never_cache(views.AquiferRetrieveUpdateAPIView.as_view()),
        name='aquifer-retrieve-update-v1'
        ),

    url(r'api/v2/aquifers/(?P<aquifer_id>[0-9]+)$',
        never_cache(views_v2.AquiferRetrieveUpdateAPIViewV2.as_view()),
        name='aquifer-retrieve-update-v2'
        ),

    # Documents (aquifer records)
    url(api_path_prefix() + r'/aquifers/(?P<aquifer_id>[0-9]+)/files$',
        never_cache(views.ListFiles.as_view()), name='aquifer-file-list'),

    # Change history for an aquifer
    url(api_path_prefix() + r'/aquifers/(?P<aquifer_id>[0-9]+)/history$',
        never_cache(views.AquiferHistory.as_view()), name='aquifer-history'),

    # Document Uploading (aquifer records)
    url(api_path_prefix() + r'/aquifers/(?P<aquifer_id>[0-9]+)/presigned_put_url$',
        never_cache(views.PreSignedDocumentKey.as_view()), name='aquifer-pre-signed-url'),

    # Document Deleting (aquifer records)
    url(api_path_prefix() + r'/aquifers/(?P<aquifer_id>[0-9]+)/delete_document$',
        never_cache(views.DeleteAquiferDocument.as_view()), name='aquifer-delete-document'),

    # Shapefile (aquifer geometry)
    url(api_path_prefix() + r'/aquifers/(?P<aquifer_id>[0-9]+)/geometry$',
        never_cache(views.SaveAquiferGeometry.as_view()), name='aquifer-save-geometry'),

    url(api_path_prefix() + r'/aquifers/sections$',
        cache_page(CACHE_TTL)(
            views.AquiferResourceSectionListAPIView.as_view()),
        name='aquifer-section-list'
        ),

    url(api_path_prefix() + r'/aquifer-codes/materials$',
        cache_page(CACHE_TTL)(views.AquiferMaterialListAPIView.as_view()),
        name='aquifer-material-list'
        ),

    url(api_path_prefix() + r'/aquifer-codes/quality-concerns$',
        cache_page(CACHE_TTL)(views.QualityConcernListAPIView.as_view()),
        name='quality-concern-list'
        ),

    url(api_path_prefix() + r'/aquifer-codes/vulnerability$',
        cache_page(CACHE_TTL)(views.AquiferVulnerabilityListAPIView.as_view()),
        name='aquifer-vulnerability-code-list'
        ),

    url(api_path_prefix() + r'/aquifer-codes/subtypes$',
        cache_page(CACHE_TTL)(views.AquiferSubtypeListAPIView.as_view()),
        name='aquifer-subtype-list'
        ),

    url(api_path_prefix() + r'/aquifer-codes/productivity$',
        cache_page(CACHE_TTL)(views.AquiferProductivityListAPIView.as_view()),
        name='aquifer-productivity-code-list'
        ),

    url(api_path_prefix() + r'/aquifer-codes/demand$',
        cache_page(CACHE_TTL)(views.AquiferDemandListAPIView.as_view()),
        name='aquifer-demand-list'
        ),

    url(api_path_prefix() + r'/aquifer-codes/water-use$',
        cache_page(CACHE_TTL)(views.WaterUseListAPIView.as_view()),
        name='aquifer-water-use-code-list'
        ),

    # The /aquifers-simplified endpoint only exists in v1. In V2 we use vector tiles instead
    url(r'api/v1/gis/aquifers-simplified$',
        views.aquifer_geojson_simplified_v1, name='aquifer-geojson-simplified-v1'),

    # GeoJSON aquifers endpoint for DataBC.
    url(r'api/v1/gis/aquifers$',
        views.aquifer_geojson_v1, name='aquifer-geojson-v1'),

    # GeoJSON aquifers endpoint for DataBC.
    url(r'api/v2/gis/aquifers$',
        views_v2.aquifer_geojson_v2, name='aquifer-geojson-v2'),
]
