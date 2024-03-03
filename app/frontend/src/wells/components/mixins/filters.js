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
/* Shared logic for handling search filters. */
import { mapGetters } from 'vuex'
import { WELL_TAGS_PRIVATE, WELL_TAGS_PUBLIC, } from '../../../common/constants'
const SEARCH_FIELDS = {
  matchAny: {
    param: 'match_any',
    type: 'radio',
    options: [
      { text: 'Any field match', value: 'true' },
      { text: 'All field match', value: 'false' }
    ]
  },
  well: {
    param: 'well',
    label: 'Well tag or ID plate number',
    type: 'text',
    sortable: true,
  },
  licenceNumber: {
    param: "licence_number",
    label: "Licence number",
    type: "number",
    resultLabel: "Licence number(s)",
    sortable: false,
  },
  wellDocumentType: {
    param: "well_document_type",
    label: "Contains document type",
    type: "select",
    options: [...WELL_TAGS_PUBLIC, ...WELL_TAGS_PRIVATE].sort((a, b) => {
      if (a.text === 'Other') return 1;
      if (b.text === 'Other') return -1;
      return a.text.toLowerCase().localeCompare(b.text.toLowerCase())
    }),
    sortable: false,
  },
  streetOrCity: {
    param: 'street_address_or_city',
    label: 'Street address or city',
    type: 'text',
    sortable: true,
  },
  ownerName: {
    param: 'owner_full_name',
    label: 'Well owner',
    resultLabel: 'Owner name',
    type: 'text',
    sortable: true,
  },
  publicationStatus: {
    param: 'well_publication_status',
    authenticated: true,
    label: 'Publication status',
    type: 'select',
    textField: 'description',
    valueField: 'well_publication_status_code',
    sortable: true,
  },
  legal: {
    param: 'legal',
    label: 'Lot, Legal plan, District lot or PID',
    type: 'text',
    sortable: true,
  },
  landDistrict: {
    param: 'land_district',
    label: 'Land district',
    type: 'select',
    sortable: true,
  },
  wellStatus: {
    param: 'well_status',
    label: 'Well status',
    type: 'select',
    textField: 'description',
    valueField: 'well_status_code',
    sortable: true,
  },
  licencedStatus: {
    param: 'licenced_status',
    label: 'Well licence status',
    type: 'select',
    textField: 'description',
    valueField: 'licenced_status_code',
    sortable: false,
  },
  personResponsible: {
    param: 'person_responsible_name',
    sortParam: 'person_responsible__name',
    label: 'Person responsible for work',
    type: 'text',
    sortable: true,
  },
  personResponsibleGuid: {
    param: 'person_responsible',
    label: 'Person responsible for work',
    type: 'select',
    textField: 'name',
    valueField: 'person_guid',
    sortable: true,
  },
  orgResponsible: {
    param: 'company_of_person_responsible_name',
    sortParam: 'company_of_person_responsible__name',
    label: 'Company that did the work',
    type: 'text',
    sortable: true,
  },
  orgResponsibleGuid: {
    param: 'company_of_person_responsible',
    label: 'Company that did the work',
    type: 'select',
    textField: 'name',
    valueField: 'org_guid',
    sortable: true,
  },
  dateOfWork: {
    param: 'date_of_work',
    label: 'Date of work',
    type: 'dateRange',
    sortable: true,
  },
  wellDepth: {
    param: 'well_depth',
    label: 'Well depth',
    type: 'range',
    sortable: false,
  },
  aquiferNr: {
    param: 'aquifer',
    label: 'Aquifer number',
    type: 'number',
    sortable: true,
  },
  wellActivityType: {
    param: 'well_activity_type',
    label: 'Well Activity Type',
    type: 'select',
    textField: 'description',
    valueField: 'code',
    sortable: true,
  },
  wellClass: {
    param: 'well_class',
    label: 'Class of well',
    type: 'select',
    textField: 'description',
    valueField: 'well_class_code',
    sortable: true,
  },
  wellSubclass: {
    param: 'well_subclass',
    label: 'Well subclass',
    type: 'select',
    sortable: true,
  },
  intendedWaterUse: {
    param: 'intended_water_use',
    label: 'Intended water use',
    type: 'select',
    textField: 'description',
    valueField: 'intended_water_use_code',
    sortable: true,
  },
  boundaryEffect: {
    param: 'boundary_effect',
    label: 'Boundary effect',
    type: 'select',
    textField: 'description',
    valueField: 'code',
    sortable: true,
  },
  wellIdPlateAttached: {
    param: 'well_identification_plate_attached',
    label: 'Where ID plate attached',
    type: 'text',
    sortable: true,
  },
  idPlateAttachedBy: {
    param: 'id_plate_attached_by',
    label: 'ID plate attached by',
    type: 'text',
    sortable: true,
  },
  waterSupplySystemName: {
    param: 'water_supply_system_name',
    label: 'Water supply system name',
    type: 'text',
    sortable: true,
  },
  waterSupplyWellName: {
    param: 'water_supply_system_well_name',
    label: 'Water supply well name',
    type: 'text',
    sortable: true,
  },
  drillerName: {
    param: 'driller_name',
    label: 'Person who completed the work',
    type: 'text',
    sortable: true,
  },
  consultantName: {
    param: 'consultant_name',
    label: 'Consultant name',
    type: 'text',
    sortable: false,
  },
  consultantCompany: {
    param: 'consultant_company',
    label: 'Consultant company',
    type: 'text',
    sortable: false,
  },
  ownerMailingAddress: {
    authenticated: true,
    param: 'owner_mailing_address',
    label: 'Owner mailing address',
    type: 'text',
    sortable: true,
  },
  ownerCity: {
    authenticated: true,
    param: 'owner_city',
    label: 'Owner city',
    type: 'text',
    sortable: true,
  },
  ownerProvince: {
    authenticated: true,
    param: 'owner_province_state',
    label: 'Owner province',
    type: 'select',
    textField: 'description',
    valueField: 'province_state_code',
    sortable: true,
  },
  ownerPostalCode: {
    authenticated: true,
    param: 'owner_postal_code',
    label: 'Owner postal code',
    type: 'text',
    sortable: true,
  },
  legalBlock: { param: 'legal_block', label: 'Block', type: 'text' },
  legalSection: { param: 'legal_section', label: 'Section', type: 'text' },
  legalTownship: { param: 'legal_township', label: 'Township', type: 'text' },
  legalRange: { param: 'legal_range', label: 'Range', type: 'text' },
  locationDescription: {
    param: 'well_location_description',
    label: 'Description of well location',
    type: 'text',
    sortable: true,
  },
  coordinateAcquisitionCode: {
    param: 'coordinate_acquisition_code',
    label: 'Coordinate acquisition type',
    type: 'select',
    textField: 'description',
    valueField: 'code',
    sortable: true,
  },
  groundElevation: {
    param: 'ground_elevation',
    label: 'Ground elevation',
    type: 'range',
    sortable: true,
  },
  groundElevationMethod: {
    param: 'ground_elevation_method',
    label: 'Method for determining ground elevation',
    type: 'select',
    textField: 'description',
    valueField: 'ground_elevation_method_code',
    sortable: true,
  },
  drillingMethods: {
    param: 'drilling_methods',
    label: 'Drilling methods',
    type: 'select',
    textField: 'description',
    valueField: 'drilling_method_code',
    sortable: true,
  },
  wellOrientationStatus: {
    param: 'well_orientation_status',
    label: 'Orientation of well',
    type: 'select',
    textField: 'description',
    valueField: 'well_orientation_code',
    sortable: true,
  },
  surfaceSealMaterial: {
    param: 'surface_seal_material',
    label: 'Suface seal material',
    type: 'select',
    textField: 'description',
    valueField: 'surface_seal_material_code',
    sortable: true,
  },
  surfaceSealDepth: {
    param: 'surface_seal_depth',
    label: 'Surface seal depth',
    type: 'range',
    sortable: true,
  },
  surfaceSealThickness: {
    param: 'surface_seal_thickness',
    label: 'Surface seal thickness',
    type: 'range',
    sortable: true,
  },
  surfaceSealMethod: {
    param: 'surface_seal_method',
    label: 'Surface seal method of installation',
    type: 'select',
    textField: 'description',
    valueField: 'surface_seal_method_code',
    sortable: true,
  },
  backfillAboveSurfaceSeal: {
    param: 'backfill_above_surface_seal',
    label: 'Backfill material above surface seal',
    type: 'text',
    sortable: false,
  },
  backfillDepth: {
    param: 'backfill_depth',
    label: 'Backfill depth',
    type: 'range',
    sortable: true,
  },
  linerMaterial: {
    param: 'liner_material',
    label: 'Liner material',
    type: 'select',
    textField: 'description',
    valueField: 'code',
    sortable: true,
  },
  linerDiameter: {
    param: 'liner_diameter',
    label: 'Liner diameter',
    type: 'range',
    sortable: true,
  },
  linerThickness: {
    param: 'liner_thickness',
    label: 'Liner thickness',
    type: 'range',
    sortable: true,
  },
  linerFrom: {
    param: 'liner_from',
    label: 'Liner from',
    type: 'range',
    sortable: true,
  },
  linerTo: {
    param: 'liner_to',
    label: 'Liner to',
    type: 'range',
    sortable: true,
  },
  linerRange: {
    param: 'liner_range',
    label: 'Liner from/to',
    type: 'range',
    sortable: true,
  },
  screenIntakeMethod: {
    param: 'screen_intake_method',
    label: 'Screen intake',
    type: 'select',
    textField: 'description',
    valueField: 'screen_intake_code',
    sortable: true,
  },
  screenType: {
    param: 'screen_type',
    label: 'Screen type',
    type: 'select',
    textField: 'description',
    valueField: 'screen_type_code',
    sortable: true,
  },
  screenMaterial: {
    param: 'screen_material',
    label: 'Screen material',
    type: 'select',
    textField: 'description',
    valueField: 'screen_material_code',
    sortable: true,
  },
  otherScreenMaterial: {
    param: 'other_screen_material',
    label: 'Screen other material',
    type: 'text',
    sortable: true,
  },
  screenOpening: {
    param: 'screen_opening',
    label: 'Screen opening',
    type: 'select',
    textField: 'description',
    valueField: 'screen_opening_code',
    sortable: true,
  },
  screenBottom: {
    param: 'screen_bottom',
    label: 'Screen bottom',
    type: 'select',
    textField: 'description',
    valueField: 'screen_bottom_code',
    sortable: true,
  },
  screenInformation: {
    param: 'screen_information',
    label: 'Screen information',
    type: 'text',
    sortable: true,
  },
  filterPackFrom: {
    param: 'filter_pack_from',
    label: 'Filter pack from',
    type: 'range',
    sortable: true,
  },
  filterPackTo: {
    param: 'filter_pack_to',
    label: 'Filter pack to',
    type: 'range',
    sortable: true,
  },
  filterPackRange: {
    param: 'filter_pack_range',
    label: 'Filter pack from/to',
    type: 'range',
    sortable: true,
  },
  filterPackMaterial: {
    param: 'filter_pack_material',
    label: 'Filter pack material',
    type: 'select',
    textField: 'description',
    valueField: 'filter_pack_material_code',
    sortable: true,
  },
  filterPackMaterialSize: {
    param: 'filter_pack_material_size',
    label: 'Filter pack material size',
    type: 'select',
    textField: 'description',
    valueField: 'filter_pack_material_size_code',
    sortable: true,
  },
  developmentMethods: {
    param: 'development_methods',
    label: 'Well development method',
    type: 'select',
    textField: 'description',
    valueField: 'development_method_code',
    sortable: true,
  },
  developmentHours: {
    param: 'development_hours',
    label: 'Development hours',
    type: 'range',
    sortable: true,
  },
  developmentNotes: {
    param: 'development_notes',
    label: 'Development notes',
    type: 'text',
    sortable: true,
  },
  yieldEstimationMethod: {
    param: 'yield_estimation_method',
    label: 'Yield estimation method',
    type: 'select',
    textField: 'description',
    valueField: 'yield_estimation_method_code',
    sortable: true,
  },
  yieldEstimationRate: {
    param: 'yield_estimation_rate',
    label: 'Yield estimation rate',
    type: 'range',
    sortable: true,
  },
  yieldEstimationDuration: {
    param: 'yield_estimation_duration',
    label: 'Yield estimation duration',
    type: 'range',
    sortable: true,
  },
  staticLevelBeforeTest: {
    param: 'static_level_before_test',
    label: 'SWL before test',
    type: 'range',
    sortable: true,
  },
  hydroFracturingPerformed: {
    param: 'hydro_fracturing_performed',
    label: 'Hydro-fracturing performed',
    type: 'radio',
    options: [{ text: 'Yes', value: 'true' }, { text: 'No', value: 'false' }],
    sortable: true,
  },
  hydroFracturingYieldIncrease: {
    param: 'hydro_fracturing_yield_increase',
    label: 'Increase in well yield',
    type: 'range',
    sortable: true,
  },
  drawdown: {
    param: 'drawdown',
    label: 'Drawdown',
    type: 'range',
    sortable: true,
  },
  recommendedPumpDepth: {
    param: 'recommended_pump_depth',
    label: 'Recommended pump depth',
    type: 'range',
    sortable: true,
  },
  recommendedPumpRate: {
    param: 'recommended_pump_rate',
    label: 'Recommended pump rate',
    type: 'range',
    sortable: true,
  },
  waterQualityCharacteristics: {
    param: 'water_quality_characteristics',
    label: 'Water quality characteristics',
    type: 'select',
    textField: 'description',
    valueField: 'code',
    sortable: true,
  },
  waterQualityColour: {
    param: 'water_quality_colour',
    label: 'Water quality colour',
    type: 'select',
    textField: 'description',
    valueField: 'code',
    sortable: true,
  },
  waterQualityOdour: {
    param: 'water_quality_odour',
    label: 'Water quality odour',
    type: 'text',
    sortable: true,
  },
  ems: {
    param: 'ems',
    label: 'EMS Id',
    type: 'text',
    anyValueBoolean: true,
    sortable: true,
  },
  finalCasingStickUp: {
    param: 'final_casing_stick_up',
    label: 'Final casing stick up',
    type: 'range',
    sortable: true,
  },
  bedrockDepth: {
    param: 'bedrock_depth',
    label: 'Depth to bedrock',
    type: 'range',
    sortable: true,
  },
  staticWaterLevel: {
    param: 'static_water_level',
    label: 'Static water level',
    type: 'range',
    sortable: true,
  },
  wellYield: {
    param: 'well_yield',
    label: 'Estimated well yield',
    type: 'range',
    sortable: true,
  },
  artesianConditions: {
    param: 'artesian_conditions',
    label: 'Artesian Condition',
    type: 'radio',
    options: [{ text: 'Yes', value: 'true' }, { text: 'No', value: 'false' }],
    sortable: true,
  },
  wellCapType: {
    param: 'well_cap_type',
    label: 'Well cap type',
    type: 'text',
    sortable: true,
  },
  observationWellNumber: {
    param: 'observation_well_number',
    label: 'Observation well number',
    type: 'text',
    anyValueBoolean: true,
    sortable: true,
  },
  observationWellStatus: {
    param: 'observation_well_status',
    label: 'Observation well status',
    type: 'select',
    textField: 'description',
    valueField: 'obs_well_status_code',
    sortable: true,
  },
  finishedWellDepth: {
    param: 'finished_well_depth',
    label: 'Finished well depth',
    resultLabel: 'Finished well depth (feet)',
    type: 'range',
    sortable: true,
  },
  decommissionReason: {
    param: 'decommission_reason',
    label: 'Reason for well decommission',
    type: 'text',
    sortable: true,
  },
  decommissionMethod: {
    param: 'decommission_method',
    label: 'Decommission method',
    type: 'select',
    textField: 'description',
    valueField: 'decommission_method_code',
    sortable: true,
  },
  decommissionSealantMaterial: {
    param: 'decommission_sealant_material',
    label: 'Sealant material',
    type: 'text',
    sortable: true,
  },
  decommissionBackfillMaterial: {
    param: 'decommission_backfill_material',
    label: 'Backfill material',
    type: 'text',
    sortable: true,
  },
  decommissionDetails: {
    param: 'decommission_details',
    label: 'Decommission details',
    type: 'text',
    sortable: true,
  },
  comments: { 
    param: 'comments',
    label: 'Comments',
    type: 'text',
    sortable: false,
  },
  alternativeSpecsSubmitted: {
    param: 'alternative_specs_submitted',
    label: 'Alt specs submitted',
    type: 'radio',
    options: [{ text: 'Yes', value: 'true' }, { text: 'No', value: 'false' }],
    sortable: true,
  },
  technicalReport: {
    param: 'technical_report',
    label: 'Technical Report',
    type: 'radio',
    options: [{ text: 'Yes', value: 'true' }, { text: 'No', value: 'false' }],
    sortable: true,
  },
  drinkingWaterProtectionArea: {
    param: 'drinking_water_protection_area_ind',
    label: 'Drinking Water Area Indicator',
    type: 'radio',
    options: [{ text: 'Yes', value: 'true' }, { text: 'No', value: 'false' }],
    sortable: true,
  },
  internalComments: {
    param: 'internal_comments',
    authenticated: true,
    label: 'Internal office comments',
    type: 'text',
    sortable: true,
  },
  aquiferLithology: {
    param: 'aquifer_lithology',
    label: 'Aquifer lithology',
    type: 'select',
    textField: 'description',
    valueField: 'aquifer_lithology_code',
    sortable: true,
  },
  aquiferVulnerabilityIndex: {
    param: 'aquifer_vulnerability_index',
    label: 'AVI',
    type: 'range',
    sortable: true,
  },
  storativity: {
    param: 'storativity',
    label: 'Storativity',
    type: 'range',
    sortable: true,
  },
  startDatePumpingTest: {
    param: 'start_date_pumping_test',
    label: 'Start Date Pumping Test',
    type: 'dateRange'
  },
  transmissivity: {
    param: 'transmissivity',
    label: 'Transmissivity',
    type: 'range',
    sortable: true,
  },
  hydraulicConductivity: {
    param: 'hydraulic_conductivity',
    label: 'Hydraulic Conductivity',
    type: 'range',
    sortable: true,
  },
  specificStorage: {
    param: 'specific_storage',
    label: 'Specific Storage',
    type: 'text',
    sortable: true,
  },
  specificYield: {
    param: 'specific_yield',
    label: 'Specific Yield',
    type: 'range',
    sortable: true,
  },
  specificCapacity: {
    param: 'specific_capacity',
    label: 'Specific Capacity',
    type: 'range',
    sortable: false,
  },
  pumpingTestDescription: {
    param: 'pumping_test_description',
    label: 'Pumping Test Description',
    type: 'select',
    textField: 'description',
    valueField: 'pumping_test_description_code',
    sortable: false,
  },
  createUser: {
    authenticated: true,
    param: 'create_user',
    label: 'Created by',
    type: 'text',
    sortable: true,
  },
  createDate: {
    authenticated: true,
    param: 'create_date',
    label: 'Created date',
    type: 'dateRange',
    sortable: true,
  },
  updateUser: {
    authenticated: true,
    param: 'update_user',
    label: 'Updated by',
    type: 'text',
    sortable: true,
  },
  updateDate: {
    authenticated: true,
    param: 'update_date',
    label: 'Updated date',
    type: 'dateRange',
    sortable: true,
  },
  wellTagNumber: {
    param: 'well_tag_number',
    label: 'Well tag number',
    type: 'text',
    sortable: true,
  },
  identificationPlateNumber: {
    param: 'identification_plate_number',
    label: 'ID plate number',
    type: 'text',
    sortable: true,
  },
  streetAddress: {
    param: 'street_address',
    label: 'Street Address',
    type: 'text',
    sortable: true,
  },
  legalLot: {
    param: 'legal_lot',
    label: 'Legal lot',
    resultLabel: 'Lot',
    type: 'text',
    sortable: true,
  },
  legalPlan: {
    param: 'legal_plan',
    label: 'Legal plan',
    resultLabel: 'Plan',
    type: 'text',
    sortable: true,
  },
  legalDistrictLot: {
    param: 'legal_district_lot',
    label: 'District lot',
    type: 'text',
    sortable: true,
  },
  legalPid: {
    param: 'legal_pid',
    label: 'PID',
    type: 'text',
    sortable: false,
  },
  diameter: {
    param: 'diameter',
    label: 'Diameter (inches)',
    type: 'range',
    sortable: true,
  },
  constructionStartDate: {
    param: 'construction_start_date',
    label: 'Construction start date',
    type: 'dateRange',
    sortable: true,
  },
  constructionEndDate: {
    param: 'construction_end_date',
    label: 'Construction end date',
    type: 'dateRange',
    sortable: true,
  },
  alterationStartDate: {
    param: 'alteration_start_date',
    label: 'Alteration start date',
    type: 'dateRange',
    sortable: true,
  },
  alterationEndDate: {
    param: 'alteration_end_date',
    label: 'Alteration end date',
    type: 'dateRange',
    sortable: true,
  },
  decomissionStartDate: {
    param: 'decomission_start_date',
    label: 'Decomission start date',
    type: 'dateRange',
    sortable: false,
  },
  decomissionEndDate: {
    param: 'decomission_end_date',
    label: 'Decomission end date',
    type: 'dateRange',
    sortable: false,
  },
  wellDisinfectedStatus: {
    param: 'well_disinfected_status',
    label: 'Well disinfected',
    type: 'select',
    textField: 'description',
    valueField: 'well_disinfected_code',
    sortable: true,
  },
  latitude: { param: 'latitude', label: 'Latitude', type: 'number' },
  longitude: { param: 'longitude', label: 'Longitude', type: 'number' },
  geocodeDistance: {
    param: 'geocode_distance',
    label: 'Geocode Distance',
    type: 'range',
    sortable: true,
  },
  distanceToPid: {
    param: 'distance_to_pid',
    label: 'Distance to Matching PID',
    type: 'range',
    sortable: true,
  },
  scoreAddress: {
    param: 'score_address',
    label: 'Score Address',
    type: 'range',
    sortable: true,
  },
  scoreCity: {
    param: 'score_city',
    label: 'Score City',
    type: 'range',
    sortable: true,
  },
  naturalResourceRegion: {
    param: 'natural_resource_region',
    label: 'Natural Resource Region',
    type: 'select',
    sortable: true,
  },
  finishedWellDepthNull: {
    param: 'finished_well_depth',
    label: 'Finished well depth',
    type: 'nullcheck'
  },
  intendedWaterUseNull: {
    param: 'intended_water_use',
    label: 'Intended water use',
    type: 'nullcheck'
  },
  wellClassNull: {
    param: 'well_class',
    label: 'Class of well',
    type: 'nullcheck'
  },
  latitudeNull: {
    param: 'latitude',
    label: 'Latitude',
    type: 'nullcheck'
  },
  longitudeNull: {
    param: 'longitude',
    label: 'Longitude',
    type: 'nullcheck'
  },
  diameterNull: {
    param: 'diameter',
    label: 'Casing Diameter (inches)',
    type: 'nullcheck'
  },
  surfaceSealDepthNull: {
    param: 'surface_seal_depth',
    label: 'Seal Depth (feet)',
    type: 'nullcheck'
  },
  surfaceSealThicknessNull: {
    param: 'surface_seal_thickness',
    label: 'Seal Thickness (inches)',
    type: 'nullcheck'
  },
  aquiferLithologyNull: {
    param: 'aquifer_lithology',
    label: 'Lithology',
    type: 'nullcheck'
  },
  workStartDateNull: {
    param: 'work_start_date',
    label: 'Work Start Date',
    type: 'nullcheck'
  },
  workEndDateNull: {
    param: 'work_end_date',
    label: 'Work End Date',
    type: 'nullcheck'
  },
  crossReferencedBy: {
    param: 'cross_referenced_by',
    label: 'Cross Referenced By',
    type: 'text',
    sortable: true
  },
  crossReferencedDate: {
    param: 'cross_referenced_date',
    label: 'Cross Referenced Date',
    type: 'dateRange',
    sortable: true
  }
}

export default {
  data() {
    return {
      filterParams: {} // filterId: {param1: val, param2: val}
    }
  },
  computed: {
    ...mapGetters([
      'codes',
      'drillerNames',
      'organizationNames',
      'userRoles'
    ]),
    searchFields() {
      const fields = { ...SEARCH_FIELDS }
      Object.keys(fields).forEach(k => {
        fields[k].sortParam = fields[k].sortParam || fields[k].param
      })

      if (!(this.userRoles.wells && this.userRoles.wells.view)) {
        Object.entries(fields).forEach(([fieldId, field]) => {
          if (field.authenticated) {
            delete fields[fieldId]
          }
        })
      }

      return fields
    },
    landDistrictOptions() {
      if (this.codes.land_district_codes === undefined || (this.codes.land_district_codes && Object.entries(this.codes.land_district_codes).length === 0)) {
        return []
      }
      return this.codes.land_district_codes.map((district) => {
        return {
          value: district.land_district_code,
          text: `${district.land_district_code} - ${district.name}`
        }
      })
    },
    wellSubclassOptions() {
      if (!this.codes.well_classes) {
        return []
      }
      const options = []
      this.codes.well_classes.forEach((wellClass) => {
        wellClass.wellsubclasscode_set.forEach((wellSubclass) => {
          options.push({
            value: wellSubclass.well_subclass_guid,
            text: `${wellClass.description} - ${wellSubclass.description}`
          })
        })
      })

      return options
    },
    filterSelectOptions() {
      const options = {
        aquiferLithology: this.codes.aquifer_lithology_codes || [],
        coordinateAcquisitionCode: this.codes.coordinate_acquisition_codes || [],
        decommissionMethod: this.codes.decommission_methods || [],
        developmentMethods: this.codes.development_methods || [],
        drillingMethods: this.codes.drilling_methods || [],
        filterPackMaterial: this.codes.filter_pack_material || [],
        filterPackMaterialSize: this.codes.filter_pack_material_size || [],
        groundElevationMethod: this.codes.ground_elevation_methods || [],
        intendedWaterUse: this.codes.intended_water_uses || [],
        boundaryEffect: this.codes.boundary_effect_codes || [],
        pumpingTestDescription: this.codes.pumping_test_description_codes || [],
        landDistrict: this.landDistrictOptions,
        licencedStatus: this.codes.licenced_status_codes || [],
        linerMaterial: this.codes.liner_material_codes || [],
        observationWellStatus: this.codes.observation_well_status || [],
        orgResponsibleGuid: this.organizationNames || [],
        ownerProvince: this.codes.province_codes || [],
        personResponsibleGuid: this.drillerNames || [],
        publicationStatus: this.codes.well_publication_status_codes || [],
        screenIntakeMethod: this.codes.screen_intake_methods || [],
        screenBottom: this.codes.screen_bottoms || [],
        screenMaterial: this.codes.screen_materials || [],
        screenOpening: this.codes.screen_openings || [],
        screenType: this.codes.screen_types || [],
        surfaceSealMaterial: this.codes.surface_seal_materials || [],
        surfaceSealMethod: this.codes.surface_seal_methods || [],
        waterQualityCharacteristics: this.codes.water_quality_characteristics || [],
        waterQualityColour: this.codes.water_quality_colours || [],
        wellActivityType: this.codes.activity_types || [],
        wellClass: this.codes.well_classes || [],
        wellDisinfectedStatus: this.codes.well_disinfected_codes || [],
        wellStatus: this.codes.well_status_codes || [],
        wellSubclass: this.wellSubclassOptions,
        yieldEstimationMethod: this.codes.yield_estimation_methods || [],
        naturalResourceRegion: ['Northeast', 'West Coast', 'South Coast', 'Omineca',
          'Skeena', 'Thompson-Okanagan', 'Cariboo', 'Kootenay']
      }

      Object.keys(options).forEach(optionId => {
        if (!this.searchFields.hasOwnProperty(optionId)) {
          delete options[optionId]
        }
      })

      return options
    },
    searchQueryParams() {
      const searchQueryParams = Object.entries(this.filterParams).reduce((allParams, [id, filterParams]) => {
        return Object.assign(allParams, filterParams)
      }, {})

      return searchQueryParams
    },
    emptyFilterParams() {
      const filterParams = {}
      Object.keys(this.searchFields).forEach(id => {
        filterParams[id] = {}
      })

      return filterParams
    }
  },
  methods: {
    getParamNames({ param, type, anyValueBoolean }) {
      const params = []
      if (type === 'range') {
        params.push(`${param}_min`, `${param}_max`)
      } else if (type === 'dateRange') {
        params.push(`${param}_after`, `${param}_before`)
      } else {
        params.push(param)
      }

      if (anyValueBoolean) {
        params.push(`${param}_has_value`)
      }

      return params
    },
    getFilterFields(fieldIds) {
      return fieldIds.filter(id => this.searchFields[id] !== undefined).map(id => {
        const field = this.searchFields[id]
        const params = this.getParamNames(field)
        return { ...field, params: params, id: id }
      })
    },
    clearFilterParams() {
      this.filterParams = { ...this.emptyFilterParams }
    }
  }
}
