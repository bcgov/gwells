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
import logging
import sys
from posixpath import join as urljoin

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Prefetch
import rest_framework.exceptions
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.views import APIView

from gwells.documents import MinioClient
from gwells.urls import app_root
from gwells.pagination import APILimitOffsetPagination
from wells.permissions import (
    WellsEditPermissions, WellsSubmissionPermissions, WellsSubmissionViewerPermissions)
from gwells.models import ProvinceStateCode
from gwells.models.lithology import (
    LithologyColourCode, LithologyHardnessCode,
    LithologyMaterialCode, LithologyMoistureCode, LithologyDescriptionCode)
from gwells.serializers import ProvinceStateCodeSerializer
from gwells.settings.base import get_env_variable
from gwells.views import AuditCreateMixin
from wells.models import (
    ActivitySubmission,
    CasingCode,
    CasingMaterialCode,
    CoordinateAcquisitionCode,
    DecommissionMaterialCode,
    DecommissionMethodCode,
    DevelopmentMethodCode,
    DrillingMethodCode,
    WellDisinfectedCode,
    WellOrientationCode,
    BoundaryEffectCode,
    DriveShoeCode,
    FilterPackMaterialCode,
    FilterPackMaterialSizeCode,
    GroundElevationMethodCode,
    IntendedWaterUseCode,
    LandDistrictCode,
    LicencedStatusCode,
    LinerMaterialCode,
    ObsWellStatusCode,
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
    WellStatusCode,
    WellPublicationStatusCode,
    YieldEstimationMethodCode,
    AquiferLithologyCode,
)
from submissions.models import WellActivityCode
from wells.serializers import (
    CasingCodeSerializer,
    CasingMaterialSerializer,
)
from submissions.serializers import (
    AlterationSubmissionDisplaySerializer,
    CoordinateAcquisitionCodeSerializer,
    ConstructionSubmissionDisplaySerializer,
    DecommissionMaterialCodeSerializer,
    DecommissionMethodCodeSerializer,
    DecommissionSubmissionDisplaySerializer,
    DevelopmentMethodCodeSerializer,
    DrillingMethodCodeSerializer,
    WellDisinfectedCodeSerializer,
    WellOrientationCodeSerializer,
    BoundaryEffectCodeSerializer,
    DriveShoeCodeSerializer,
    FilterPackMaterialCodeSerializer,
    FilterPackMaterialSizeCodeSerializer,
    GroundElevationMethodCodeSerializer,
    IntendedWaterUseCodeSerializer,
    LandDistrictSerializer,
    LegacyWellDisplaySerializer,
    LinerMaterialCodeSerializer,
    LithologyHardnessSerializer,
    LithologyColourSerializer,
    LithologyDescriptionCodeSerializer,
    LithologyMaterialSerializer,
    LithologyMoistureSerializer,
    ObservationWellStatusCodeSerializer,
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
    WellConstructionSubmissionSerializer,
    WellAlterationSubmissionSerializer,
    WellDecommissionSubmissionSerializer,
    WellSubmissionListSerializer,
    WellActivityCodeSerializer,
    WellClassCodeSerializer,
    WellStatusCodeSerializer,
    WellPublicationStatusCodeSerializer,
    WellSubclassCodeSerializer,
    YieldEstimationMethodCodeSerializer,
    WellStaffEditSubmissionSerializer,
    AquiferLithologySerializer,
    LicencedStatusCodeSerializer,
)


logger = logging.getLogger(__name__)


def get_submission_queryset(qs):
    return qs.select_related(
                "well_class",
                "well_subclass",
                "intended_water_use",
                "person_responsible",
                'company_of_person_responsible',
                "owner_province_state",
                "ground_elevation_method",
                "surface_seal_material",
                "surface_seal_method",
                "liner_material",
            ) \
            .prefetch_related(
                "water_quality_characteristics",
                "lithologydescription_set",
                "linerperforation_set",
                "casing_set",
                "screen_set",
                "decommission_description_set",
                "drilling_methods"
            ) \
            .order_by("filing_number")


class SubmissionGetAPIView(RetrieveAPIView):
    """Get a submission"""

    permission_classes = (WellsSubmissionViewerPermissions,)
    queryset = ActivitySubmission.objects.all()
    model = ActivitySubmission
    lookup_field = 'filing_number'

    def get_serializer(self, *args, **kwargs):
        serializer_class = WellSubmissionListSerializer
        kwargs['context'] = self.get_serializer_context()

        # this method is called with the first argument being the ActivitySubmission object to be serialized

        if len(args) == 0:
            return serializer_class(*args, **kwargs)

        data = args[0]
        activity = data.well_activity_type.code

        # There are different serializers; which one is used depends on well_activity_type
        if activity and activity == WellActivityCode.types.construction().code:
            serializer_class = ConstructionSubmissionDisplaySerializer
        elif activity and activity == WellActivityCode.types.alteration().code:
            serializer_class = AlterationSubmissionDisplaySerializer
        elif activity and activity == WellActivityCode.types.decommission().code:
            serializer_class = DecommissionSubmissionDisplaySerializer
        elif activity and activity == WellActivityCode.types.legacy().code:
            serializer_class = LegacyWellDisplaySerializer

        return serializer_class(*args, **kwargs)


class SubmissionListAPIView(ListAPIView):
    """List submissions

    get: returns a list of well activity submissions
    """

    permission_classes = (WellsSubmissionViewerPermissions,)
    model = ActivitySubmission
    queryset = ActivitySubmission.objects.all()
    pagination_class = APILimitOffsetPagination
    serializer_class = WellSubmissionListSerializer

    def get_queryset(self):
        return get_submission_queryset(self.queryset)

    def list(self, request, **kwargs):
        """ List activity submissions with pagination """
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = WellSubmissionListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = WellSubmissionListSerializer(filtered_queryset, many=True)
        return Response(serializer.data)


class SubmissionBase(AuditCreateMixin, ListCreateAPIView):
    """ Base class for mutating data that has detailed error logging.
    """

    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except rest_framework.exceptions.APIException as error:
            try:
                logger.warning(('Problem encountered handling POST; '
                                'user:{request.user.profile.username}; '
                                'user.is_authenticated:{request.user.is_authenticated}; '
                                'path:{request.path}; method:{request.method}; status_code:{error.status_code}; '
                                'request: {request.data}; '
                                'response: {error.detail}').format(
                    request=request,
                    error=error))
            except:
                logger.error('Error logging error!', exc_info=sys.exc_info())
            raise
        except:
            try:
                logger.warning(('Problem encountered handling POST; '
                             'user:{request.user.profile.username}; '
                             'user.is_authenticated:{request.user.is_authenticated}; '
                             'path:{request.path}; method:{request.method};'
                             'request: {request.data}; '
                             'detail: {detail}').format(
                    request=request,
                    detail=sys.exc_info()))
            except:
                logger.error('Error logging error!', exc_info=sys.exc_info())
            raise


class SubmissionConstructionAPIView(SubmissionBase):
    """Create a construction submission"""

    model = ActivitySubmission
    serializer_class = WellConstructionSubmissionSerializer
    permission_classes = (WellsSubmissionPermissions,)
    queryset = ActivitySubmission.objects.all()

    def get_queryset(self):
        return get_submission_queryset(self.queryset)\
            .filter(well_activity_type=WellActivityCode.types.construction())


class SubmissionAlterationAPIView(SubmissionBase):
    """Create an alteration submission"""

    model = ActivitySubmission
    serializer_class = WellAlterationSubmissionSerializer
    permission_classes = (WellsSubmissionPermissions,)
    queryset = ActivitySubmission.objects.all()

    def get_queryset(self):
        return get_submission_queryset(self.queryset)\
            .filter(well_activity_type=WellActivityCode.types.alteration())


class SubmissionDecommissionAPIView(SubmissionBase):
    """Create a decommission submission"""

    model = ActivitySubmission
    serializer_class = WellDecommissionSubmissionSerializer
    permission_classes = (WellsSubmissionPermissions,)
    queryset = ActivitySubmission.objects.all()

    def get_queryset(self):
        return get_submission_queryset(self.queryset)\
            .filter(well_activity_type=WellActivityCode.types.decommission())


class SubmissionStaffEditAPIView(SubmissionBase):
    """ Create a staff edit submission"""
    model = ActivitySubmission
    serializer_class = WellStaffEditSubmissionSerializer
    permission_classes = (WellsEditPermissions,)
    queryset = ActivitySubmission.objects.all()

    def post(self, request, *args, **kwargs):
        # ground_elevation is a decimal so we swap empty string with null value
        if 'ground_elevation' in request.data:
            if request.data['ground_elevation'] == '':
                request.data['ground_elevation'] = None
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return get_submission_queryset(self.queryset)\
            .filter(well_activity_type=WellActivityCode.types.staff_edit())


class SubmissionsOptions(APIView):
    """Options required for submitting activity report forms"""

    swagger_schema = None

    def get(self, request, **kwargs):
        options = {}
        now = timezone.now()

        province_codes = ProvinceStateCodeSerializer(
            instance=ProvinceStateCode.objects.all(), many=True)
        activity_codes = WellActivityCodeSerializer(
            instance=WellActivityCode.objects.all(), many=True)
        well_class_codes = WellClassCodeSerializer(
            instance=WellClassCode.objects.prefetch_related(Prefetch('wellsubclasscode_set',
                                                                     queryset=WellSubclassCode.objects.filter(expiry_date__gt=now),
                                                                     to_attr='all_well_subclass_codes')).filter(expiry_date__gt=now), many=True)
        intended_water_use_codes = IntendedWaterUseCodeSerializer(
            instance=IntendedWaterUseCode.objects.all(), many=True)
        casing_codes = CasingCodeSerializer(
            instance=CasingCode.objects.all(), many=True)
        casing_material = CasingMaterialSerializer(
            instance=CasingMaterialCode.objects.all(), many=True)
        decommission_materials = DecommissionMaterialCodeSerializer(
            instance=DecommissionMaterialCode.objects.all(), many=True)
        decommission_methods = DecommissionMethodCodeSerializer(
            instance=DecommissionMethodCode.objects.all(), many=True)
        well_disinfected_codes = WellDisinfectedCodeSerializer(
            instance=WellDisinfectedCode.objects.all(), many=True)
        well_orientation_codes = WellOrientationCodeSerializer(
            instance=WellOrientationCode.objects.all(), many=True)
        boundary_effect_codes = BoundaryEffectCodeSerializer(
            instance=BoundaryEffectCode.objects.all(), many=True)
        drive_shoe_codes = DriveShoeCodeSerializer(
            instance=DriveShoeCode.objects.all(), many=True)
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
        well_status_codes = WellStatusCodeSerializer(
            instance=WellStatusCode.objects.all(), many=True
        )
        well_publication_status_codes = WellPublicationStatusCodeSerializer(
            instance=WellPublicationStatusCode.objects.all(), many=True
        )
        coordinate_acquisition_codes = CoordinateAcquisitionCodeSerializer(
            instance=CoordinateAcquisitionCode.objects.all(), many=True)
        observation_well_status = ObservationWellStatusCodeSerializer(
            instance=ObsWellStatusCode.objects.all(), many=True
        )
        aquifer_lithology = AquiferLithologySerializer(instance=AquiferLithologyCode.objects.all(), many=True)

        lithology_hardness = LithologyHardnessSerializer(
            instance=LithologyHardnessCode.objects.all(), many=True)
        lithology_colours = LithologyColourSerializer(instance=LithologyColourCode.objects.all(), many=True)
        lithology_materials = LithologyMaterialSerializer(
            instance=LithologyMaterialCode.objects.all(), many=True)
        lithology_moisture = LithologyMoistureSerializer(
            instance=LithologyMoistureCode.objects.all(), many=True)
        lithology_descriptors = LithologyDescriptionCodeSerializer(
            instance=LithologyDescriptionCode.objects.all(), many=True)
        licenced_status_codes = LicencedStatusCodeSerializer(
            instance=LicencedStatusCode.objects.all(), many=True)

        root = urljoin('/', app_root, 'api/v2/')
        for item in activity_codes.data:
            if item['code'] not in ('LEGACY'):
                item['path'] = reverse(item['code'], kwargs={'version': 'v2'})[len(root):]

        options["province_codes"] = province_codes.data
        options["activity_types"] = activity_codes.data
        options["coordinate_acquisition_codes"] = coordinate_acquisition_codes.data
        options["well_classes"] = well_class_codes.data
        options["intended_water_uses"] = intended_water_use_codes.data
        options["casing_codes"] = casing_codes.data
        options["casing_materials"] = casing_material.data
        options["decommission_materials"] = decommission_materials.data
        options["decommission_methods"] = decommission_methods.data
        options["well_disinfected_codes"] = well_disinfected_codes.data
        options["well_orientation_codes"] = well_orientation_codes.data
        options["boundary_effect_codes"] = boundary_effect_codes.data
        options["drive_shoe_codes"] = drive_shoe_codes.data
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
        options["aquifer_lithology_codes"] = aquifer_lithology.data
        options["lithology_hardness_codes"] = lithology_hardness.data
        options["lithology_colours"] = lithology_colours.data
        options["lithology_materials"] = lithology_materials.data
        options["lithology_moisture_codes"] = lithology_moisture.data
        options["lithology_descriptors"] = lithology_descriptors.data
        options["well_status_codes"] = well_status_codes.data
        options["well_publication_status_codes"] = well_publication_status_codes.data
        options["observation_well_status"] = observation_well_status.data
        options["licenced_status_codes"] = licenced_status_codes.data

        return Response(options)


class PreSignedDocumentKey(RetrieveAPIView):
    """
    Get a pre-signed document key to upload into an S3 compatible document store

    post: obtain a URL that is pre-signed to allow client-side uploads
    """

    queryset = ActivitySubmission.objects.all()
    permission_classes = (WellsSubmissionPermissions,)

    def get(self, request, submission_id, **kwargs):
        submission = get_object_or_404(self.queryset, pk=submission_id)

        client = MinioClient(
            request=request, disable_private=False)

        object_name = request.GET.get("filename")
        filename = client.format_object_name(object_name, int(submission.well.well_tag_number), "well")
        bucket_name = get_env_variable("S3_ROOT_BUCKET")

        is_private = False
        if request.GET.get("private") == "true":
            is_private = True
            bucket_name = get_env_variable("S3_PRIVATE_ROOT_BUCKET")

        url = client.get_presigned_put_url(
            filename, bucket_name=bucket_name, private=is_private)

        return JsonResponse({"object_name": object_name, "url": url})
