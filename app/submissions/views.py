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

from rest_framework.response import Response
from django.views.generic import TemplateView
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView

from gwells.pagination import APILimitOffsetPagination
from wells.permissions import WellsPermissions
from gwells.models import ProvinceStateCode
from gwells.serializers import ProvinceStateCodeSerializer
from wells.models import (
    ActivitySubmission,
    IntendedWaterUseCode,
    Well,
    WellClassCode,
    WellSubclassCode)
from submissions.models import WellActivityCode
from submissions.serializers import (
    WellSubmissionSerializer,
    WellActivityCodeSerializer,
    WellClassCodeSerializer,
    WellSubclassCodeSerializer,
    IntendedWaterUseCodeSerializer
)


class SubmissionListAPIView(ListCreateAPIView):
    """List and create submissions

    get: returns a list of well activity submissions
    post: adds a new submission
    """

    permission_classes = (WellsPermissions,)
    model = ActivitySubmission
    queryset = ActivitySubmission.objects.all()
    pagination_class = APILimitOffsetPagination
    serializer_class = WellSubmissionSerializer

    def get_queryset(self):
        qs = self.queryset
        qs = qs \
            .select_related(
                "well_class",
                "well_subclass",
                "intended_water_use",
                "driller_responsible",
                "owner_province_state",
                "ground_elevation_method",
                "drilling_method",
                "surface_seal_material",
                "surface_seal_method",
                "liner_material",
            ) \
            .prefetch_related(
                "water_quality_characteristics",
                "lithologydescription_set",
                "linerperforation_set",
                "productiondata_set",
                "casing_set",
                "screen_set",
            ) \
            .order_by("filing_number")
        return qs

    def list(self, request):
        """ List activity submissions with pagination """
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = WellSubmissionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = WellSubmissionSerializer(filtered_queryset, many=True)
        return Response(serializer.data)


class SubmissionsOptions(APIView):
    """Options required for submitting activity report forms"""

    def get(self, request):
        options = {}

        province_codes = ProvinceStateCodeSerializer(
            instance=ProvinceStateCode.objects.all(), many=True)
        activity_codes = WellActivityCodeSerializer(
            instance=WellActivityCode.objects.all(), many=True)
        well_class_codes = WellClassCodeSerializer(
            instance=WellClassCode.objects.prefetch_related("wellsubclasscode_set"), many=True)
        intended_water_use_codes = IntendedWaterUseCodeSerializer(
            instance=IntendedWaterUseCode.objects.all(), many=True)

        options["province_codes"] = province_codes.data
        options["activity_types"] = activity_codes.data
        options["well_classes"] = well_class_codes.data
        options["intended_water_uses"] = intended_water_use_codes.data

        return Response(options)


class SubmissionsHomeView(TemplateView):
    """Loads the html file containing the Submissions web app"""
    template_name = 'submissions/submissions.html'
