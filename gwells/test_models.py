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
from .models import *

from django.test import TestCase

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
        filter_pack_material = FilterPackMaterial()
        self.assertIsInstance(filter_pack_material, FilterPackMaterial)

    def test_filter_pack_material_size_instantiation(self):
        filter_pack_material_size = FilterPackMaterialSize()
        self.assertIsInstance(filter_pack_material_size, FilterPackMaterialSize)

    def test_ground_elevation_method_instantiation(self):
        ground_elevation_method = GroundElevationMethod()
        self.assertIsInstance(ground_elevation_method, GroundElevationMethod)

    def test_intended_water_use_instantiation(self):
        intended_water_use = IntendedWaterUse()
        self.assertIsInstance(intended_water_use, IntendedWaterUse)

    def test_land_district_instantiation(self):
        land_district = LandDistrict()
        self.assertIsInstance(land_district, LandDistrict)

    def test_licenced_status_instantiation(self):
        licenced_status = LicencedStatus()
        self.assertIsInstance(licenced_status, LicencedStatus)

    def test_liner_material_instantiation(self):
        liner_material = LinerMaterial()
        self.assertIsInstance(liner_material, LinerMaterial)

    def test_liner_perforation_instantiation(self):
        liner_perforation = LinerPerforation()
        self.assertIsInstance(liner_perforation, LinerPerforation)

    def test_lithology_colour_instantiation(self):
        lithology_colour = LithologyColour()
        self.assertIsInstance(lithology_colour, LithologyColour)

    def test_lithology_description_instantiation(self):
        lithology_description = LithologyDescription()
        self.assertIsInstance(lithology_description, LithologyDescription)

    def test_lithology_description_code_instantiation(self):
        lithology_description_code = LithologyDescriptionCode()
        self.assertIsInstance(lithology_description_code, LithologyDescriptionCode)

    def test_lithology_hardness_instantiation(self):
        lithology_hardness = LithologyHardness()
        self.assertIsInstance(lithology_hardness, LithologyHardness)

    def test_lithology_material_instantiation(self):
        lithology_material = LithologyMaterial()
        self.assertIsInstance(lithology_material, LithologyMaterial)

    def test_lithology_moisture_instantiation(self):
        lithology_moisture = LithologyMoisture()
        self.assertIsInstance(lithology_moisture, LithologyMoisture)

    def test_lithology_structure_instantiation(self):
        lithology_structure = LithologyStructure()
        self.assertIsInstance(lithology_structure, LithologyStructure)

    def test_ltsa_owner_instantiation(self):
        ltsa_owner = LtsaOwner()
        self.assertIsInstance(ltsa_owner, LtsaOwner)

    def test_observation_well_status_instantiation(self):
        observation_well_status = ObservationWellStatus()
        self.assertIsInstance(observation_well_status, ObservationWellStatus)

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
        screen_assembly_type = ScreenAssemblyType()
        self.assertIsInstance(screen_assembly_type, ScreenAssemblyType)

    def test_screen_bottom_instantiation(self):
        screen_bottom = ScreenBottom()
        self.assertIsInstance(screen_bottom, ScreenBottom)

    def test_screen_intake_method_instantiation(self):
        screen_intake_method = ScreenIntakeMethod()
        self.assertIsInstance(screen_intake_method, ScreenIntakeMethod)

    def test_screen_material_instantiation(self):
        screen_material = ScreenMaterial()
        self.assertIsInstance(screen_material, ScreenMaterial)

    def test_screen_opening_instantiation(self):
        screen_opening = ScreenOpening()
        self.assertIsInstance(screen_opening, ScreenOpening)

    def test_screen_type_instantiation(self):
        screen_type = ScreenType()
        self.assertIsInstance(screen_type, ScreenType)

    def test_surface_seal_material_instantiation(self):
        surface_seal_material = SurfaceSealMaterial()
        self.assertIsInstance(surface_seal_material, SurfaceSealMaterial)

    def test_surface_seal_method_instantiation(self):
        surface_seal_method = SurfaceSealMethod()
        self.assertIsInstance(surface_seal_method, SurfaceSealMethod)

    def test_surficial_material_instantiation(self):
        surficial_material = SurficialMaterial()
        self.assertIsInstance(surficial_material, SurficialMaterial)

    def test_water_quality_characteristic_instantiation(self):
        water_quality_characteristic = WaterQualityCharacteristic()
        self.assertIsInstance(water_quality_characteristic, WaterQualityCharacteristic)

    def test_well_instantiation(self):
        well = Well()
        self.assertIsInstance(well, Well)

    def test_well_activity_type_instantiation(self):
        well_activity_type = WellActivityType()
        self.assertIsInstance(well_activity_type, WellActivityType)

    def test_well_class_instantiation(self):
        well_class = WellClass()
        self.assertIsInstance(well_class, WellClass)

    def test_well_status_instantiation(self):
        well_status = WellStatus()
        self.assertIsInstance(well_status, WellStatus)

    def test_well_subclass_instantiation(self):
        well_subclass = WellSubclass()
        self.assertIsInstance(well_subclass, WellSubclass)

    def test_well_yield_unit_instantiation(self):
        well_yield_unit = WellYieldUnit()
        self.assertIsInstance(well_yield_unit, WellYieldUnit)

    def test_yield_estimation_method_instantiation(self):
        yield_estimation_method = YieldEstimationMethod()
        self.assertIsInstance(yield_estimation_method, YieldEstimationMethod)
