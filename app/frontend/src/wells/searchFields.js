/*
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/

const searchFields = {
  default: [
    {
      header: 'Search By',
      fields: [
        { id: 'matchAny', param: 'match_any', type: 'radio', options: [{ text: 'Any field match', value: 'true' }, { text: 'All field match', value: 'false' }] },
        { id: 'well', param: 'well', label: 'Well tag or ID plate number', type: 'text' },
        { id: 'streetOrCity', param: 'street_address_or_city', label: 'Street address or city', type: 'text' },
        { id: 'ownerName', param: 'owner_full_name', label: 'Well owner', type: 'text' }
      ]
    },
    {
      header: 'Location',
      fields: [
        { id: 'legal', param: 'legal', label: 'Lot, Legal plan, District lot or PID', type: 'text' },
        { id: 'landDistrict', param: 'land_district', label: 'Land district', type: 'select' }
      ]
    },
    {
      header: 'Well Details',
      fields: [
        { id: 'wellStatus', param: 'well_status', label: 'Well status', type: 'select', textField: 'description', valueField: 'well_status_code' },
        { id: 'licencedStatus', param: 'licenced_status', label: 'Well licence status', type: 'select', textField: 'description', valueField: 'licenced_status_code' },
        { id: 'personResponsible', param: 'person_responsible', label: 'Person responsible for work', type: 'select', textField: 'name', valueField: 'person_guid' },
        { id: 'orgResponsible', param: 'company_of_person_responsible', label: 'Company that did the work', type: 'select', textField: 'name', valueField: 'org_guid' },
        { id: 'dateOfWork', param: 'date_of_work', label: 'Date of work', type: 'dateRange' },
        { id: 'wellDepth', param: 'well_depth', label: 'Well depth', type: 'range' }
      ]
    },
    {
      header: 'Aquifer',
      fields: [
        { id: 'aquiferNr', param: 'aquifer', label: 'Aquifer number', type: 'number' }
      ]
    }
  ],
  optional: [
    {
      header: 'Well Class',
      fields: [
        { id: 'wellClass', param: 'well_class', label: 'Class of well', type: 'select', textField: 'description', valueField: 'well_class_code' },
        { id: 'wellSubclass', param: 'well_subclass', label: 'Well subclass', type: 'select' },
        { id: 'intendedWaterUse', param: 'intended_water_use', label: 'Intended water use', type: 'select', textField: 'description', valueField: 'intended_water_use_code' },
        { id: 'wellIdPlateAttached', param: 'well_identification_plate_attached', label: 'Where ID plate attached', type: 'text' },
        { id: 'idPlateAttachedBy', param: 'id_plate_attached_by', label: 'ID plate attached by', type: 'text' },
        { id: 'waterSupplySystemName', param: 'water_supply_system_name', label: 'Water supply system name', type: 'text' },
        { id: 'waterSupplyWellName', param: 'water_supply_system_well_name', label: 'Water supply well name', type: 'text' },
        { id: 'publicationStatus', param: 'well_publication_status', authenticated: true, label: 'Publication status', type: 'select', textField: 'description', valueField: 'well_publication_status_code' }
      ]
    },
    {
      header: 'Person responsible for work',
      fields: [
        { id: 'drillerName', param: 'driller_name', label: 'Person who completed the work', type: 'text' },
        { id: 'consultantName', param: 'consultant_name', label: 'Consultant name', type: 'text' },
        { id: 'consultantCompany', param: 'consultant_company', label: 'Consultant company', type: 'text' }
      ]
    },
    {
      header: 'Well owner',
      authenticated: true,
      fields: [
        { id: 'ownerMailingAddress', param: 'owner_mailing_address', label: 'Owner mailing address', type: 'text' },
        { id: 'ownerCity', param: 'owner_city', label: 'Owner city', type: 'text' },
        { id: 'ownerProvince', param: 'owner_province_state', label: 'Owner province', type: 'select', textField: 'description', valueField: 'province_state_code' },
        { id: 'ownerPostalCode', param: 'owner_postal_code', label: 'Owner postal code', type: 'text' }
      ]
    },
    {
      header: 'Well location',
      fields: [
        { id: 'legalBlock', param: 'legal_block', label: 'Block', type: 'text' },
        { id: 'legalSection', param: 'legal_section', label: 'Section', type: 'text' },
        { id: 'legalTownship', param: 'legal_township', label: 'Township', type: 'text' },
        { id: 'legalRange', param: 'legal_range', label: 'Range', type: 'text' },
        { id: 'locationDescription', param: 'well_location_description', label: 'Description of well location', type: 'text' }
      ]
    },
    {
      header: 'Geocoordinates',
      fields: [
        { id: 'coordinateAcquisitionCode', param: 'coordinate_acquisition_code', label: 'Coordinate acquisition type', type: 'select', textField: 'description', valueField: 'code' }
      ]
    },
    {
      header: 'Method of drilling',
      fields: [
        { id: 'groundElevation', param: 'ground_elevation', label: 'Ground elevation', type: 'range' },
        { id: 'groundElevationMethod', param: 'ground_elevation_method', label: 'Method for determining ground elevation', type: 'select', textField: 'description', valueField: 'ground_elevation_method_code' },
        { id: 'drillingMethods', param: 'drilling_methods', label: 'Drilling methods', type: 'select', textField: 'description', valueField: 'drilling_method_code' },
        { id: 'wellOrientation', param: 'well_orientation', label: 'Orientation of well', type: 'radio', options: [{ text: 'Vertical', value: 'true' }, { text: 'Horizontal', value: 'false' }] }
      ]
    },
    {
      header: 'Surface seal and backfill material',
      fields: [
        { id: 'surfaceSealMaterial', param: 'surface_seal_material', label: 'Suface seal material', type: 'select', textField: 'description', valueField: 'surface_seal_material_code' },
        { id: 'surfaceSealDepth', param: 'surface_seal_depth', label: 'Surface seal depth', type: 'range' },
        { id: 'surfaceSealThickness', param: 'surface_seal_thickness', label: 'Surface seal thickness', type: 'range' },
        { id: 'surfaceSealMethod', param: 'surface_seal_method', label: 'Surface seal method of installation', type: 'select', textField: 'description', valueField: 'surface_seal_method_code' },
        { id: 'backfillAboveSurfaceSeal', param: 'backfill_above_surface_seal', label: 'Backfill material above surface seal', type: 'text' },
        { id: 'backfillDepth', param: 'backfill_depth', label: 'Backfill depth', type: 'range' }
      ]
    },
    {
      header: 'Liner information',
      fields: [
        { id: 'linerMaterial', param: 'liner_material', label: 'Liner material', type: 'select', textField: 'description', valueField: 'liner_material_code' },
        { id: 'linerDiameter', param: 'liner_diameter', label: 'Liner diameter', type: 'range' },
        { id: 'linerThickness', param: 'liner_thickness', label: 'Liner thickness', type: 'range' },
        { id: 'linerRange', param: 'liner_range', label: 'Liner from/to', type: 'range' }
      ]
    },
    {
      header: 'Screen information',
      fields: [
        { id: 'screenIntakeMethod', param: 'screen_intake_method', label: 'Screen intake', type: 'select', textField: 'description', valueField: 'screen_intake_code' },
        { id: 'screenType', param: 'screen_type', label: 'Screen type', type: 'select', textField: 'description', valueField: 'screen_type_code' },
        { id: 'screenMaterial', param: 'screen_material', label: 'Screen material', type: 'select', textField: 'description', valueField: 'screen_material_code' },
        { id: 'otherScreenMaterial', param: 'other_screen_material', label: 'Screen other material', type: 'text' },
        { id: 'screenOpening', param: 'screen_opening', label: 'Screen opening', type: 'select', textField: 'description', valueField: 'screen_opening_code' },
        { id: 'screenBottom', param: 'screen_bottom', label: 'Screen bottom', type: 'select', textField: 'description', valueField: 'screen_bottom_code' },
        { id: 'screenInformation', param: 'screen_information', label: 'Screen information', type: 'text' }
      ]
    },
    {
      header: 'Filter pack',
      fields: [
        { id: 'filterPackRange', param: 'filter_pack_range', label: 'Filter pack from/to', type: 'range' },
        { id: 'filterPackMaterial', param: 'filter_pack_material', label: 'Filter pack material', type: 'select', textField: 'description', valueField: 'filter_pack_material_code' },
        { id: 'filterPackMaterialSize', param: 'filter_pack_material_size', label: 'Filter pack material size', type: 'select', textField: 'description', valueField: 'filter_pack_material_size_code' }
      ]
    },
    {
      header: 'Well development',
      fields: [
        { id: 'developmentMethods', param: 'development_methods', label: 'Well development method', type: 'select', textField: 'description', valueField: 'development_method_code' },
        { id: 'developmentHours', param: 'development_hours', label: 'Development hours', type: 'range' },
        { id: 'developmentNotes', param: 'development_notes', label: 'Development notes', type: 'text' }
      ]
    },
    {
      header: 'Yield',
      fields: [
        { id: 'yieldEstimationMethod', param: 'yield_estimation_method', label: 'Yield estimation method', type: 'select', textField: 'description', valueField: 'yield_estimation_method_code' },
        { id: 'yieldEstimationRate', param: 'yield_estimation_rate', label: 'Yield estimation rate', type: 'range' },
        { id: 'yieldEstimationDuration', param: 'yield_estimation_duration', label: 'Yield estimation duration', type: 'range' },
        { id: 'staticLevelBeforeTest', param: 'static_level_before_test', label: 'SWL before test', type: 'range' },
        { id: 'hydroFracturingPerformed', param: 'hydro_fracturing_performed', label: 'Hydro-fracturing performed', type: 'radio', options: [{ text: 'Yes', value: 'true' }, { text: 'No', value: 'false' }] },
        { id: 'hydroFracturingYieldIncrease', param: 'hydro_fracturing_yield_increase', label: 'Increase in well yield', type: 'range' },
        { id: 'drawdown', param: 'drawdown', label: 'Drawdown', type: 'range' },
        { id: 'recommendedPumpDepth', param: 'recommended_pump_depth', label: 'Recommended pump depth', type: 'range' },
        { id: 'recommendedPumpRate', param: 'recommended_pump_rate', label: 'Recommended pump rate', type: 'range' }
      ]
    },
    {
      header: 'Water quality',
      fields: [
        { id: 'waterQualityCharacteristics', param: 'water_quality_characteristics', label: 'Water quality characteristics', type: 'select', textField: 'description', valueField: 'code' },
        { id: 'waterQualityColour', param: 'water_quality_colour', label: 'Water quality colour', type: 'select', textField: 'description', valueField: 'code' },
        { id: 'waterQualityOdor', param: 'water_quality_odor', label: 'Water quality odor', type: 'text' },
        { id: 'ems', param: 'ems', label: 'EMS Id', type: 'text' }
      ]
    },
    {
      header: 'Well completion data',
      fields: [
        { id: 'finalCasingStickUp', param: 'final_casing_stick_up', label: 'Final casing stick up', type: 'range' },
        { id: 'bedrockDepth', param: 'bedrock_depth', label: 'Depth to bedrock', type: 'range' },
        { id: 'staticWaterLevel', param: 'static_water_level', label: 'Static water level', type: 'range' },
        { id: 'wellYield', param: 'well_yield', label: 'Estimated well yield', type: 'range' },
        { id: 'artesianFlow', param: 'artesian_flow', label: 'Artesian flow', type: 'range' },
        { id: 'artesianPressure', param: 'artesian_pressure', label: 'Artesian pressure', type: 'range' },
        { id: 'wellCapType', param: 'well_cap_type', label: 'Well cap type', type: 'text' },
        { id: 'wellDisinfected', param: 'well_disinfected', label: 'Well disinfected', type: 'radio', options: [{ text: 'Yes', value: 'true' }, { text: 'No', value: 'false' }] }
      ]
    },
    {
      header: 'Observation well information',
      fields: [
        { id: 'observationWellNumber', param: 'observation_well_number', label: 'Observation well number', type: 'text' },
        { id: 'observationWellStatus', param: 'observation_well_status', label: 'Observation well status', type: 'select', textField: 'description', valueField: 'obs_well_status_code' }
      ]
    },
    {
      header: 'Decommission',
      fields: [
        { id: 'finishedWellDepth', param: 'finished_well_depth', label: 'Finished well depth - decommission', type: 'range' },
        { id: 'decommissionReason', param: 'decommission_reason', label: 'Reason for well decommission', type: 'text' },
        { id: 'decommissionMethod', param: 'decommission_method', label: 'Decommission method', type: 'select', textField: 'description', valueField: 'decommission_method_code' },
        { id: 'decommissionSealantMaterial', param: 'decommission_sealant_material', label: 'Sealant material', type: 'text' },
        { id: 'decommissionBackfillMaterial', param: 'decommission_backfill_material', label: 'Backfill material', type: 'text' },
        { id: 'decommissionDetails', param: 'decommission_details', label: 'Decommission details', type: 'text' }
      ]
    },
    {
      header: 'Comments',
      fields: [
        { id: 'comments', param: 'comments', label: 'Comments', type: 'text' },
        { id: 'alternativeSpecsSubmitted', param: 'alternative_specs_submitted', label: 'Alt specs submitted', type: 'radio', options: [{ text: 'Yes', value: 'true' }, { text: 'No', value: 'false' }] },
        { id: 'internalComments', param: 'internal_comments', authenticated: true, label: 'Internal office comments', type: 'text' }
      ]
    },
    {
      header: 'Well testing and aquifer details',
      fields: [
        { id: 'aquiferLithology', param: 'aquifer_lithology', label: 'Aquifer lithology', type: 'select', textField: 'description', valueField: 'aquifer_lithology_code' },
        { id: 'aquiferVulnerabilityIndex', param: 'aquifer_vulnerability_index', label: 'AVI', type: 'range' },
        { id: 'storativity', param: 'storativity', label: 'Storativity', type: 'range' },
        { id: 'transmissivity', param: 'transmissivity', label: 'Transmissivity', type: 'range' },
        { id: 'hydraulicConductivity', param: 'hydraulic_conductivity', label: 'Hydraulic Conductivity', type: 'text' },
        { id: 'specificStorage', param: 'specific_storage', label: 'Specific Storage', type: 'text' },
        { id: 'specificYield', param: 'specific_yield', label: 'Specific Yield', type: 'range' },
        { id: 'testingMethod', param: 'testing_method', label: 'Testing method', type: 'text' },
        { id: 'testingDuration', param: 'testing_duration', label: 'Testing duration', type: 'range' },
        { id: 'analyticSolutionType', param: 'analytic_solution_type', label: 'Analytic solution', type: 'range' },
        { id: 'boundaryEffect', param: 'boundary_effect', label: 'Boundary effect', type: 'range' }
      ]
    },
    {
      header: 'Record maintenance',
      authenticated: true,
      fields: [
        { id: 'createUser', param: 'create_user', label: 'Created by', type: 'text' },
        { id: 'createDate', param: 'create_date', label: 'Created date', type: 'dateRange' },
        { id: 'updateUser', param: 'update_user', label: 'Updated by', type: 'text' },
        { id: 'updateDate', param: 'update_date', label: 'Updated date', type: 'dateRange' }
      ]
    }
  ]
}

export default searchFields
