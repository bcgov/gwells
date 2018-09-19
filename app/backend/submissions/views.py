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
from wells.permissions import WellsEditPermissions
from gwells.models import ProvinceStateCode
from gwells.serializers import ProvinceStateCodeSerializer
from wells.models import (
    ActivitySubmission,
    CasingCode,
    CasingMaterialCode,
    DevelopmentMethodCode,
    DrillingMethodCode,
    FilterPackMaterialCode,
    FilterPackMaterialSizeCode,
    GroundElevationMethodCode,
    IntendedWaterUseCode,
    LandDistrictCode,
    LinerMaterialCode,
    ScreenIntakeMethodCode,
    SurfaceSealMaterialCode,
    SurfaceSealMethodCode,
    SurficialMaterialCode,
    ScreenTypeCode,
    ScreenMaterialCode,
    ScreenOpeningCode,
    ScreenBottomCode,
    ScreenAssemblyTypeCode,
    WaterQualityCharacteristic,
    WaterQualityColour,
    Well,
    WellClassCode,
    WellSubclassCode,
    YieldEstimationMethodCode,)
from submissions.models import WellActivityCode
from wells.serializers import (
    CasingCodeSerializer,
    CasingMaterialSerializer
)
from submissions.serializers import (
    DevelopmentMethodCodeSerializer,
    DrillingMethodCodeSerializer,
    FilterPackMaterialCodeSerializer,
    FilterPackMaterialSizeCodeSerializer,
    GroundElevationMethodCodeSerializer,
    IntendedWaterUseCodeSerializer,
    LandDistrictSerializer,
    LinerMaterialCodeSerializer,
    ScreenIntakeMethodSerializer,
    SurfaceSealMaterialCodeSerializer,
    SurfaceSealMethodCodeSerializer,
    SurficialMaterialCodeSerializer,
    ScreenTypeCodeSerializer,
    ScreenMaterialCodeSerializer,
    ScreenOpeningCodeSerializer,
    ScreenBottomCodeSerializer,
    ScreenAssemblyTypeCodeSerializer,
    WaterQualityCharacteristicSerializer,
    WaterQualityColourSerializer,
    WellSubmissionSerializer,
    WellActivityCodeSerializer,
    WellClassCodeSerializer,
    WellSubclassCodeSerializer,
    YieldEstimationMethodCodeSerializer,    
)


class SubmissionListAPIView(ListCreateAPIView):
    """List and create submissions

    get: returns a list of well activity submissions
    post: adds a new submission
    """

    permission_classes = (WellsEditPermissions,)
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
        casing_codes = CasingCodeSerializer(
            instance=CasingCode.objects.all(), many=True)
        casing_material = CasingMaterialSerializer(
            instance=CasingMaterialCode.objects.all(), many=True)
        filter_pack_material = FilterPackMaterialCodeSerializer(
            instance=FilterPackMaterialCode.objects.all(), many=True)
        filter_pack_material_size = FilterPackMaterialSizeCodeSerializer(
            instance=FilterPackMaterialSizeCode.objects.all(), many=True)
        land_district_codes = LandDistrictSerializer(
            instance=LandDistrictCode.objects.all(), many=True)
        liner_material_codes = LinerMaterialCodeSerializer(
            instance=LinerMaterialCode.objects.all(), many=True)
        ground_elevation_method_codes = GroundElevationMethodCodeSerializer(
            instance=GroundElevationMethodCode.objects.all(), many=True)
        drilling_method_codes = DrillingMethodCodeSerializer(
            instance=DrillingMethodCode.objects.all(), many=True)
        surface_seal_method_codes = SurfaceSealMethodCodeSerializer(
            instance=SurfaceSealMethodCode.objects.all(), many=True)
        surface_seal_material_codes = SurfaceSealMaterialCodeSerializer(
            instance=SurfaceSealMaterialCode.objects.all(), many=True)
        surficial_material_codes = SurficialMaterialCodeSerializer(
            instance=SurficialMaterialCode.objects.all(), many=True)
        screen_intake_methods = ScreenIntakeMethodSerializer(
            instance=ScreenIntakeMethodCode.objects.all(), many=True)
        screen_types = ScreenTypeCodeSerializer(instance=ScreenTypeCode.objects.all(), many=True)
        screen_materials = ScreenMaterialCodeSerializer(instance=ScreenMaterialCode.objects.all(), many=True)
        screen_openings = ScreenOpeningCodeSerializer(instance=ScreenOpeningCode.objects.all(), many=True)
        screen_bottoms = ScreenBottomCodeSerializer(instance=ScreenBottomCode.objects.all(), many=True)
        screen_assemblies = ScreenAssemblyTypeCodeSerializer(
            instance=ScreenAssemblyTypeCode.objects.all(), many=True)
        development_methods = DevelopmentMethodCodeSerializer(
            instance=DevelopmentMethodCode.objects.all(), many=True)
        yield_estimation_methods = YieldEstimationMethodCodeSerializer(
            instance=YieldEstimationMethodCode.objects.all(), many=True)
        water_quality_characteristics = WaterQualityCharacteristicSerializer(
            instance=WaterQualityCharacteristic.objects.all(), many=True)
        water_quality_colours = WaterQualityColourSerializer(
            instance=WaterQualityColour.objects.all(), many=True)

        options["province_codes"] = province_codes.data
        options["activity_types"] = activity_codes.data
        options["well_classes"] = well_class_codes.data
        options["intended_water_uses"] = intended_water_use_codes.data
        options["casing_codes"] = casing_codes.data
        options["casing_materials"] = casing_material.data
        options["filter_pack_material"] = filter_pack_material.data
        options["filter_pack_material_size"] = filter_pack_material_size.data
        options["land_district_codes"] = land_district_codes.data
        options["liner_material_codes"] = liner_material_codes.data
        options["screen_intake_methods"] = screen_intake_methods.data
        options["ground_elevation_methods"] = ground_elevation_method_codes.data
        options["drilling_methods"] = drilling_method_codes.data
        options["surface_seal_methods"] = surface_seal_method_codes.data
        options["surface_seal_materials"] = surface_seal_material_codes.data
        options["surficial_material_codes"] = surficial_material_codes.data
        options["screen_types"] = screen_types.data
        options["screen_materials"] = screen_materials.data
        options["screen_openings"] = screen_openings.data
        options["screen_bottoms"] = screen_bottoms.data
        options["screen_assemblies"] = screen_assemblies.data
        options["development_methods"] = development_methods.data
        options["yield_estimation_methods"] = yield_estimation_methods.data
        options["water_quality_characteristics"] = water_quality_characteristics.data
        options["water_quality_colours"] = water_quality_colours.data

        return Response(options)


class SubmissionsHomeView(TemplateView):
    """Loads the html file containing the Submissions web app"""
    template_name = 'submissions/submissions.html'
