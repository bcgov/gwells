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

from aquifers import views

CACHE_TTL = 60*15
api_version_url_re = '(?P<version>(v1|v2))'

urlpatterns = [
    url(rf'^api/' + api_version_url_re + r'/aquifers$',
        never_cache(views.AquiferListCreateAPIView.as_view()),
        name='aquifers-list-create'
        ),

    url(fr'^api/' + api_version_url_re + r'/aquifers/csv$',
        never_cache(views.csv_export),
        name='aquifers-list-csv'
        ),

    url(fr'^api/' + api_version_url_re + r'/aquifers/xlsx$',
        never_cache(views.xlsx_export),
        name='aquifers-list-xlsx'
        ),

    url(fr'^api/' + api_version_url_re + r'/aquifers/names$',
        never_cache(views.AquiferNameList.as_view()),
        name='aquifer-name-list'
        ),

    url(fr'^api/' + api_version_url_re + r'/aquifers/(?P<aquifer_id>[0-9]+)/edit$',
        never_cache(views.AquiferEditDetailsAPIView.as_view()),
        name='aquifer-retrieve-update'
        ),

    url(fr'^api/' + api_version_url_re + r'/aquifers/(?P<aquifer_id>[0-9]+)$',
        never_cache(views.AquiferRetrieveUpdateAPIView.as_view()),
        name='aquifer-retrieve-update'
        ),

    # Documents (aquifer records)
    url(fr'^api/' + api_version_url_re + r'/aquifers/(?P<aquifer_id>[0-9]+)/files$',
        never_cache(views.ListFiles.as_view()), name='aquifer-file-list'),

    # Change history for an aquifer
    url(fr'^api/' + api_version_url_re + r'/aquifers/(?P<aquifer_id>[0-9]+)/history$',
        never_cache(views.AquiferHistory.as_view()), name='aquifer-history'),

    # Document Uploading (aquifer records)
    url(fr'^api/' + api_version_url_re + r'/aquifers/(?P<aquifer_id>[0-9]+)/presigned_put_url$',
        never_cache(views.PreSignedDocumentKey.as_view()), name='aquifer-pre-signed-url'),

    # Document Deleting (aquifer records)
    url(fr'^api/' + api_version_url_re + r'/aquifers/(?P<aquifer_id>[0-9]+)/delete_document$',
        never_cache(views.DeleteAquiferDocument.as_view()), name='aquifer-delete-document'),

    # Shapefile (aquifer geometry)
    url(fr'^api/' + api_version_url_re + r'/aquifers/(?P<aquifer_id>[0-9]+)/geometry$',
        never_cache(views.SaveAquiferGeometry.as_view()), name='aquifer-save-geometry'),

    url(fr'^api/' + api_version_url_re + r'/aquifers/sections$',
        cache_page(CACHE_TTL)(
            views.AquiferResourceSectionListAPIView.as_view()),
        name='aquifer-section-list'
        ),

    url(fr'^api/' + api_version_url_re + r'/aquifer-codes/materials$',
        cache_page(CACHE_TTL)(views.AquiferMaterialListAPIView.as_view()),
        name='aquifer-material-list'
        ),

    url(fr'^api/' + api_version_url_re + r'/aquifer-codes/quality-concerns$',
        cache_page(CACHE_TTL)(views.QualityConcernListAPIView.as_view()),
        name='quality-concern-list'
        ),

    url(fr'^api/' + api_version_url_re + r'/aquifer-codes/vulnerability$',
        cache_page(CACHE_TTL)(views.AquiferVulnerabilityListAPIView.as_view()),
        name='aquifer-vulnerability-code-list'
        ),

    url(fr'^api/' + api_version_url_re + r'/aquifer-codes/subtypes$',
        cache_page(CACHE_TTL)(views.AquiferSubtypeListAPIView.as_view()),
        name='aquifer-subtype-list'
        ),

    url(fr'^api/' + api_version_url_re + r'/aquifer-codes/productivity$',
        cache_page(CACHE_TTL)(views.AquiferProductivityListAPIView.as_view()),
        name='aquifer-productivity-code-list'
        ),

    url(fr'^api/' + api_version_url_re + r'/aquifer-codes/demand$',
        cache_page(CACHE_TTL)(views.AquiferDemandListAPIView.as_view()),
        name='aquifer-demand-list'
        ),

    url(fr'^api/' + api_version_url_re + r'/aquifer-codes/water-use$',
        cache_page(CACHE_TTL)(views.WaterUseListAPIView.as_view()),
        name='aquifer-water-use-code-list'
        ),
    url(fr'^api/' + api_version_url_re + r'/gis/aquifers-simplified$',
        views.aquifer_geojson_simplified, name='aquifer-geojson-simplified'),

    # GeoJSON aquifers endpoint for DataBC.
    url(fr'^api/' + api_version_url_re + r'/gis/aquifers$',
        views.aquifer_geojson, name='aquifer-geojson')
]
