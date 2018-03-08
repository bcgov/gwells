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

from django.test import TestCase
from gwells.models import *
from django.contrib.auth.models import User

#TODO split the tests into one test file per class

class ModelsTestCase(TestCase):

    def test_activity_submission_instantiation(self):
        activity_submission = ActivitySubmission();
        self.assertIsInstance(activity_submission, ActivitySubmission)

    def test_aquifer_well_instantiation(self):
        aquifer_well = AquiferWell();
        self.assertIsInstance(aquifer_well, AquiferWell)

    def test_bcgs_numbers_instantiation(self):
        bcgs_numbers = BCGS_Numbers();
        self.assertIsInstance(bcgs_numbers, BCGS_Numbers)

    def test_bedrock_material_instantiation(self):
        bedrock_material= BedrockMaterialCode()
        self.assertIsInstance(bedrock_material, BedrockMaterialCode)

    def test_bedrock_material_descriptor_instantiation(self):
        bedrock_material_descriptor = BedrockMaterialDescriptorCode()
        self.assertIsInstance(bedrock_material_descriptor, BedrockMaterialDescriptorCode)

    def test_casing_instantiation(self):
        casing = Casing()
        self.assertIsInstance(casing, Casing)

    def test_casing_material_instantiation(self):
        casing_material = CasingMaterialCode()
        self.assertIsInstance(casing_material, CasingMaterialCode)

    def test_casing_code_instantiation(self):
        casing_code = CasingCode()
        self.assertIsInstance(casing_code, CasingCode)

    def test_decommission_method_instantiation(self):
        decommission_method = DecommissionMethodCode()
        self.assertIsInstance(decommission_method, DecommissionMethodCode)

    def test_development_method_instantiation(self):
        development_method = DevelopmentMethodCode()
        self.assertIsInstance(development_method, DevelopmentMethodCode)

    def test_driller_instantiation(self):
        driller = Driller()
        self.assertIsInstance(driller, Driller)

    def test_drilling_company_instantiation(self):
        drilling_company = DrillingCompany()
        self.assertIsInstance(drilling_company, DrillingCompany)

    def test_drilling_method_instantiation(self):
        drilling_method = DrillingMethodCode()
        self.assertIsInstance(drilling_method, DrillingMethodCode)

    def test_filter_pack_material_instantiation(self):
        filter_pack_material = FilterPackMaterialCode()
        self.assertIsInstance(filter_pack_material, FilterPackMaterialCode)

    def test_filter_pack_material_size_instantiation(self):
        filter_pack_material_size = FilterPackMaterialSizeCode()
        self.assertIsInstance(filter_pack_material_size, FilterPackMaterialSizeCode)

    def test_ground_elevation_method_instantiation(self):
        ground_elevation_method = GroundElevationMethodCode()
        self.assertIsInstance(ground_elevation_method, GroundElevationMethodCode)

    def test_intended_water_use_instantiation(self):
        intended_water_use = IntendedWaterUseCode()
        self.assertIsInstance(intended_water_use, IntendedWaterUseCode)

    def test_land_district_instantiation(self):
        land_district = LandDistrictCode()
        self.assertIsInstance(land_district, LandDistrictCode)

    def test_licenced_status_instantiation(self):
        licenced_status = LicencedStatusCode()
        self.assertIsInstance(licenced_status, LicencedStatusCode)

    def test_liner_material_instantiation(self):
        liner_material = LinerMaterialCode()
        self.assertIsInstance(liner_material, LinerMaterialCode)

    def test_liner_perforation_instantiation(self):
        liner_perforation = LinerPerforation()
        self.assertIsInstance(liner_perforation, LinerPerforation)

    def test_lithology_colour_instantiation(self):
        lithology_colour = LithologyColourCode()
        self.assertIsInstance(lithology_colour, LithologyColourCode)

    def test_lithology_description_instantiation(self):
        lithology_description = LithologyDescription()
        self.assertIsInstance(lithology_description, LithologyDescription)

    def test_lithology_description_code_instantiation(self):
        lithology_description_code = LithologyDescriptionCode()
        self.assertIsInstance(lithology_description_code, LithologyDescriptionCode)

    def test_lithology_hardness_instantiation(self):
        lithology_hardness = LithologyHardnessCode()
        self.assertIsInstance(lithology_hardness, LithologyHardnessCode)

    def test_lithology_material_instantiation(self):
        lithology_material = LithologyMaterialCode()
        self.assertIsInstance(lithology_material, LithologyMaterialCode)

    def test_lithology_moisture_instantiation(self):
        lithology_moisture = LithologyMoistureCode()
        self.assertIsInstance(lithology_moisture, LithologyMoistureCode)

    def test_lithology_structure_instantiation(self):
        lithology_structure = LithologyStructureCode()
        self.assertIsInstance(lithology_structure, LithologyStructureCode)

    def test_ltsa_owner_instantiation(self):
        ltsa_owner = LtsaOwner()
        self.assertIsInstance(ltsa_owner, LtsaOwner)

    def test_observation_well_status_instantiation(self):
        observation_well_status = ObsWellStatusCode()
        self.assertIsInstance(observation_well_status, ObsWellStatusCode)

    def test_perforation_instantiation(self):
        perforation = Perforation()
        self.assertIsInstance(perforation, Perforation)

    def test_production_data_instantiation(self):
        production_data = ProductionData()
        self.assertIsInstance(production_data, ProductionData)

    def test_province_state_instantiation(self):
        province_state = ProvinceStateCode()
        self.assertIsInstance(province_state, ProvinceStateCode)

    def test_screen_instantiation(self):
        screen = Screen()
        self.assertIsInstance(screen, Screen)

    def test_screen_assembly_type_instantiation(self):
        screen_assembly_type = ScreenAssemblyTypeCode()
        self.assertIsInstance(screen_assembly_type, ScreenAssemblyTypeCode)

    def test_screen_bottom_instantiation(self):
        screen_bottom = ScreenBottomCode()
        self.assertIsInstance(screen_bottom, ScreenBottomCode)

    def test_screen_intake_method_instantiation(self):
        screen_intake_method = ScreenIntakeMethodCode()
        self.assertIsInstance(screen_intake_method, ScreenIntakeMethodCode)

    def test_screen_material_instantiation(self):
        screen_material = ScreenMaterialCode()
        self.assertIsInstance(screen_material, ScreenMaterialCode)

    def test_screen_opening_instantiation(self):
        screen_opening = ScreenOpeningCode()
        self.assertIsInstance(screen_opening, ScreenOpeningCode)

    def test_screen_type_instantiation(self):
        screen_type = ScreenTypeCode()
        self.assertIsInstance(screen_type, ScreenTypeCode)

    def test_surface_seal_material_instantiation(self):
        surface_seal_material = SurfaceSealMaterialCode()
        self.assertIsInstance(surface_seal_material, SurfaceSealMaterialCode)

    def test_surface_seal_method_instantiation(self):
        surface_seal_method = SurfaceSealMethodCode()
        self.assertIsInstance(surface_seal_method, SurfaceSealMethodCode)

    def test_surficial_material_instantiation(self):
        surficial_material = SurficialMaterialCode()
        self.assertIsInstance(surficial_material, SurficialMaterialCode)

    def test_water_quality_characteristic_instantiation(self):
        water_quality_characteristic = WaterQualityCharacteristic()
        self.assertIsInstance(water_quality_characteristic, WaterQualityCharacteristic)

    def test_well_instantiation(self):
        well = Well()
        self.assertIsInstance(well, Well)

    def test_well_activity_type_instantiation(self):
        well_activity_type = WellActivityCode()
        self.assertIsInstance(well_activity_type, WellActivityCode)

    def test_well_class_instantiation(self):
        well_class = WellClassCode()
        self.assertIsInstance(well_class, WellClassCode)

    def test_well_status_instantiation(self):
        well_status = WellStatusCode()
        self.assertIsInstance(well_status, WellStatusCode)

    def test_well_subclass_instantiation(self):
        well_subclass = WellSubclassCode()
        self.assertIsInstance(well_subclass, WellSubclassCode)

    def test_well_yield_unit_instantiation(self):
        well_yield_unit = WellYieldUnitCode()
        self.assertIsInstance(well_yield_unit, WellYieldUnitCode)

    def test_yield_estimation_method_instantiation(self):
        yield_estimation_method = YieldEstimationMethodCode()
        self.assertIsInstance(yield_estimation_method, YieldEstimationMethodCode)

    def test_profile(self):
        user = User.objects.create(username="foo")
        self.assertIsInstance(user, User)
        self.assertEqual(Profile.objects.all().count(), 1)
        self.assertEqual(user, Profile.objects.all()[0].user)
