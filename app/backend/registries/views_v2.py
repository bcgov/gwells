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
import csv
import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.writer.excel import save_virtual_workbook

from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.core.exceptions import PermissionDenied
from rest_framework.decorators import api_view

from gwells.roles import REGISTRIES_VIEWER_ROLE

from .views import person_search_qs

REGISTRY_EXPORT_HEADER_COLUMNS = [
    'person_name',
    'contact_email',
    'contact_cell',
    'contact_tel',
    'well_driller_orcs_number',
    'pump_installer_orcs_number',
    'description',
    'registration_number',
    'registraiton_status',
    'primary_certificate',
    'company_name',
    'company_address',
    'company_province_state',
    'company_email',
    'company_tel',
    'company_fax',
    'company_url',
    'person_guid',
    'org_guid',
]

def build_row(queryset):
    for person in queryset:
        for registration in person.registrations.all():
            for application in registration.applications.all():
                yield [
                    person.name,
                    person.contact_email,
                    person.contact_cell,
                    person.contact_tel,
                    person.well_driller_orcs_no,
                    person.pump_installer_orcs_no,
                    application.subactivity.description,
                    registration.registration_no,
                    application.display_status,
                    application.primary_certificate,
                    registration.organization.name,
                    registration.organization.mailing_address,
                    registration.organization.province_state,
                    registration.organization.email,
                    registration.organization.main_tel,
                    registration.organization.fax_tel,
                    registration.organization.website_url,
                    person.person_guid,
                    registration.organization_id,
                ]

@api_view(['GET'])
def csv_export_v2(request):
    """
    Export the registry as CSV. This is done in a vanilla functional Django view instead
    of DRF, because DRF doesn't have native CSV support.
    """

    user_is_staff = request.user.groups.filter(name=REGISTRIES_VIEWER_ROLE).exists()
    if not user_is_staff:
        raise PermissionDenied()

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registry.csv"'
    writer = csv.writer(response)
    writer.writerow(REGISTRY_EXPORT_HEADER_COLUMNS)

    queryset = person_search_qs(request)
    for row in build_row(queryset):
        writer.writerow(row)

    return response


@api_view(['GET'])
def xlsx_export_v2(request):
    """
    Export the registry as XLSX.
    """
    mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    user_is_staff = request.user.groups.filter(name=REGISTRIES_VIEWER_ROLE).exists()
    if not user_is_staff:
        raise PermissionDenied()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(REGISTRY_EXPORT_HEADER_COLUMNS)
    for i, column_name in enumerate(REGISTRY_EXPORT_HEADER_COLUMNS):
        col_letter = get_column_letter(i + 1)
        ws.column_dimensions[col_letter].width = len(column_name)
    queryset = person_search_qs(request)
    for row in build_row(queryset):
        ws.append([str(col) if col else '' for col in row])
    response = HttpResponse(content=save_virtual_workbook(wb), content_type=mime_type)
    response['Content-Disposition'] = 'attachment; filename="registry.xlsx"'
    return response
