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

from gwells.urls import api_path_prefix
from . import views
from . import views_v2

urlpatterns = [

    # API endpoints
    # Submissions for a well
    url(api_path_prefix() + r'/wells/(?P<well_tag_number>[0-9]+)/edit$',
        never_cache(views.WellStaffEditDetail.as_view()), name='well-edit-details'),

    url(api_path_prefix() + r'/wells/(?P<well_id>[0-9]+)/history$',
        never_cache(views.WellHistory.as_view()), name='well-history'),

    # Submissions for a well
    url(api_path_prefix() + r'/wells/(?P<well_id>[0-9]+)/submissions$',
        never_cache(views.WellSubmissionsListAPIView.as_view()), name='submissions-by-well'),

    # Well's vertical aquifer extents
    url(r'api/v2/wells/(?P<well_tag_number>[0-9]+)/vertical-aquifer-extents$',
        never_cache(views_v2.WellAquiferListV2APIView.as_view()), name='well-aquifers'),

    # Well
    url(r'api/v1/wells/(?P<well_tag_number>[0-9]+)$',
        never_cache(views.WellDetail.as_view()), name='well-detail'),
    url(r'api/v2/wells/(?P<well_tag_number>[0-9]+)$',
        never_cache(views_v2.WellDetail.as_view()), name='well-detail'),

    # Well tag search
    url(api_path_prefix() + r'/wells/tags$',
        never_cache(views.WellTagSearchAPIView.as_view()), name='well-tag-search'),

    # Well screen search
    # returns information about well screens for a range of wells provided in ?wells=123,124,125 etc.
    url(api_path_prefix() + r'/wells/screens$',
        never_cache(views.WellScreens.as_view()), name='well-screens'),

    # Well subsurface search
    # returns information about well subsurface for a range of wells,
    # or a list of wells provided in ?wells=123,124,125 etc.
    url(api_path_prefix() + r'/wells/subsurface',
        never_cache(views_v2.WellSubsurface.as_view()), name='well-subsurface'),

    # Well lithology search
    # returns information about well lithology for a range of wells provided in ?wells=123,124,125 etc.
    url(api_path_prefix() + r'/wells/lithology$',
        never_cache(views.WellLithology.as_view()), name='well-lithology'),

    # Well tag search
    url(r'api/v1/wells/locations$',
        never_cache(views.WellLocationListAPIViewV1.as_view()), name='well-locations-v1'),

    url(r'api/v2/wells/locations$',
        never_cache(views_v2.WellLocationListV2APIView.as_view()), name='well-locations-v2'),

    # Documents (well records)
    url(api_path_prefix() + r'/wells/(?P<tag>[0-9]+)/files$',
        never_cache(views.ListFiles.as_view()), name='file-list'),

    # Increment/Decrement count of files for a given well during uploads
    url(api_path_prefix() + r'/wells/(?P<tag>[0-9]+)/sum$',
        never_cache(views.FileSumView.as_view()), name='file-sums'),

    # Extract files
    url(api_path_prefix() + r'/wells/extracts$', views.ListExtracts.as_view(), name='extract-list'),

    # Document Uploading (well records)
    url(api_path_prefix() + r'/wells/(?P<tag>[0-9]+)/presigned_put_url$',
        never_cache(views.PreSignedDocumentKey.as_view()), name='well-pre-signed-url'),

    # Document Uploading (well records)
    url(api_path_prefix() + r'/wells/(?P<tag>[0-9]+)/delete_document$',
        never_cache(views.DeleteWellDocument.as_view()), name='well-delete-document'),

    # Well list
    url(r'api/v1/wells$',
        never_cache(views.WellListAPIViewV1.as_view()), name='well-list-v1'),

    # Well list
    url(r'api/v2/wells$',
        never_cache(views_v2.WellListAPIViewV2.as_view()), name='well-list-v2'),

    # Well search export
    url(r'api/v1/wells/export$',
        never_cache(views.WellExportListAPIViewV1.as_view()), name='well-export-v1'),

    # Well search export
    url(r'api/v2/wells/export$',
        never_cache(views_v2.WellExportListAPIViewV2.as_view()), name='well-export-v2'),

    # GeoJSON well endpoint for DataBC.
    url(api_path_prefix() + r'/gis/wells$',
        views.well_geojson, name='well-geojson'),

    # GeoJSON lithology endpoint for DataBC.
    url(api_path_prefix() + r'/gis/lithology$',
        views.lithology_geojson, name='well-lithology-geojson'),

    # 'Pumping Test and Aquifer Parameters' endpoint for DataBC
    url(r'api/v2/gis/aquifer-parameters$',
        views.aquifer_pump_params, name='aquifers-parameters'),
    
    # Well Licensing status endpoint from e-Licensing.
    url(api_path_prefix() + r'/wells/licensing$',
        views.well_licensing, name='well-licensing'),
    
    # get geocoder address
    url(api_path_prefix() + r'/wells/geocoder$',
        views.AddressGeocoder.as_view(), name='address-geocoder'),

    # QA/QC Endpoints
    url(api_path_prefix() + r'/qaqc/crossreferencing$',
        never_cache(views_v2.CrossReferencingListView.as_view()), name='qaqc-cross-referencing'),

    url(api_path_prefix() + r'/qaqc/mislocatedwells$',
        never_cache(views_v2.MislocatedWellsListView.as_view()), name='qaqc-mislocated-wells'),

    url(api_path_prefix() + r'/qaqc/recordcompliance$',
        never_cache(views_v2.RecordComplianceListView.as_view()), name='qaqc-record-compliance'),

    # Download URLs for QA/QC Endpoints
    url(api_path_prefix() + r'/qaqc/crossreferencing/download$',
        never_cache(views_v2.CrossReferencingDownloadView.as_view()), name='qaqc-cross-referencing-download'),

    url(api_path_prefix() + r'/qaqc/mislocatedwells/download$',
        never_cache(views_v2.MislocatedWellsDownloadView.as_view()), name='qaqc-mislocated-wells-download'),

    url(api_path_prefix() + r'/qaqc/recordcompliance/download$',
        never_cache(views_v2.RecordComplianceDownloadView.as_view()), name='qaqc-record-compliance-download'),
]
