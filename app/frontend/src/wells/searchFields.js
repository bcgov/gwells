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
  matchAny: {
    param: 'match_any',
    type: 'radio',
    options: [
      { text: 'Any field match', value: 'true' },
      { text: 'All field match', value: 'false' }
    ]
  },
  well: { param: 'well', label: 'Well tag or ID plate number', type: 'text' },
  streetOrCity: {
    param: 'street_address_or_city',
    label: 'Street address or city',
    type: 'text'
  },
  ownerName: {
    param: 'owner_full_name',
    label: 'Well owner',
    resultLabel: 'Owner name',
    type: 'text'
  },
  publicationStatus: {
    param: 'well_publication_status',
    authenticated: true,
    label: 'Publication status',
    type: 'select',
    textField: 'description',
    valueField: 'well_publication_status_code'
  },
  legal: {
    param: 'legal',
    label: 'Lot, Legal plan, District lot or PID',
    type: 'text'
  },
  landDistrict: {
    param: 'land_district',
    label: 'Land district',
    type: 'select'
  },
  wellStatus: {
    param: 'well_status',
    label: 'Well status',
    type: 'select',
    textField: 'description',
    valueField: 'well_status_code'
  },
  licencedStatus: {
    param: 'licenced_status',
    label: 'Well licence status',
    type: 'select',
    textField: 'description',
    valueField: 'licenced_status_code'
  },
  personResponsible: {
    param: 'person_responsible',
    label: 'Person responsible for work',
    type: 'select',
    textField: 'name',
    valueField: 'person_guid'
  },
  orgResponsible: {
    param: 'company_of_person_responsible',
    label: 'Company that did the work',
    type: 'select',
    textField: 'name',
    valueField: 'org_guid'
  },
  dateOfWork: {
    param: 'date_of_work',
    label: 'Date of work',
    type: 'dateRange'
  },
  wellDepth: { param: 'well_depth', label: 'Well depth', type: 'range' },
  aquiferNr: { param: 'aquifer', label: 'Aquifer number', type: 'number' },
  wellClass: {
    param: 'well_class',
    label: 'Class of well',
    type: 'select',
    textField: 'description',
    valueField: 'well_class_code'
  },
  wellSubclass: {
    param: 'well_subclass',
    label: 'Well subclass',
    type: 'select'
  },
  intendedWaterUse: {
    param: 'intended_water_use',
    label: 'Intended water use',
    type: 'select',
    textField: 'description',
    valueField: 'intended_water_use_code'
  },
  wellIdPlateAttached: {
    param: 'well_identification_plate_attached',
    label: 'Where ID plate attached',
    type: 'text'
  },
  idPlateAttachedBy: {
    param: 'id_plate_attached_by',
    label: 'ID plate attached by',
    type: 'text'
  },
  waterSupplySystemName: {
    param: 'water_supply_system_name',
    label: 'Water supply system name',
    type: 'text'
  },
  waterSupplyWellName: {
    param: 'water_supply_system_well_name',
    label: 'Water supply well name',
    type: 'text'
  },
  drillerName: {
    param: 'driller_name',
    label: 'Person who completed the work',
    type: 'text'
  },
  consultantName: {
    param: 'consultant_name',
    label: 'Consultant name',
    type: 'text'
  },
  consultantCompany: {
    param: 'consultant_company',
    label: 'Consultant company',
    type: 'text'
  },
  ownerMailingAddress: {
    authenticated: true,
    param: 'owner_mailing_address',
    label: 'Owner mailing address',
    type: 'text'
  },
  ownerCity: {
    authenticated: true,
    param: 'owner_city',
    label: 'Owner city',
    type: 'text'
  },
  ownerProvince: {
    authenticated: true,
    param: 'owner_province_state',
    label: 'Owner province',
    type: 'select',
    textField: 'description',
    valueField: 'province_state_code'
  },
  ownerPostalCode: {
    authenticated: true,
    param: 'owner_postal_code',
    label: 'Owner postal code',
    type: 'text'
  },
  legalBlock: { param: 'legal_block', label: 'Block', type: 'text' },
  legalSection: { param: 'legal_section', label: 'Section', type: 'text' },
  legalTownship: { param: 'legal_township', label: 'Township', type: 'text' },
  legalRange: { param: 'legal_range', label: 'Range', type: 'text' },
  locationDescription: {
    param: 'well_location_description',
    label: 'Description of well location',
    type: 'text'
  },
  coordinateAcquisitionCode: {
    param: 'coordinate_acquisition_code',
    label: 'Coordinate acquisition type',
    type: 'select',
    textField: 'description',
    valueField: 'code'
  },
  groundElevation: {
    param: 'ground_elevation',
    label: 'Ground elevation',
    type: 'range'
  },
  groundElevationMethod: {
    param: 'ground_elevation_method',
    label: 'Method for determining ground elevation',
    type: 'select',
    textField: 'description',
    valueField: 'ground_elevation_method_code'
  },
  drillingMethods: {
    param: 'drilling_methods',
    label: 'Drilling methods',
    type: 'select',
    textField: 'description',
    valueField: 'drilling_method_code'
  },
  wellOrientation: {
    param: 'well_orientation',
    label: 'Orientation of well',
    type: 'radio',
    options: [
      { text: 'Vertical', value: 'true' },
      { text: 'Horizontal', value: 'false' }
    ]
  },
  surfaceSealMaterial: {
    param: 'surface_seal_material',
    label: 'Suface seal material',
    type: 'select',
    textField: 'description',
    valueField: 'surface_seal_material_code'
  },
  surfaceSealDepth: {
    param: 'surface_seal_depth',
    label: 'Surface seal depth',
    type: 'range'
  },
  surfaceSealThickness: {
    param: 'surface_seal_thickness',
    label: 'Surface seal thickness',
    type: 'range'
  },
  surfaceSealMethod: {
    param: 'surface_seal_method',
    label: 'Surface seal method of installation',
    type: 'select',
    textField: 'description',
    valueField: 'surface_seal_method_code'
  },
  backfillAboveSurfaceSeal: {
    param: 'backfill_above_surface_seal',
    label: 'Backfill material above surface seal',
    type: 'text'
  },
  backfillDepth: {
    param: 'backfill_depth',
    label: 'Backfill depth',
    type: 'range'
  },
  linerMaterial: {
    param: 'liner_material',
    label: 'Liner material',
    type: 'select',
    textField: 'description',
    valueField: 'liner_material_code'
  },
  linerDiameter: {
    param: 'liner_diameter',
    label: 'Liner diameter',
    type: 'range'
  },
  linerThickness: {
    param: 'liner_thickness',
    label: 'Liner thickness',
    type: 'range'
  },
  linerRange: { param: 'liner_range', label: 'Liner from/to', type: 'range' },
  screenIntakeMethod: {
    param: 'screen_intake_method',
    label: 'Screen intake',
    type: 'select',
    textField: 'description',
    valueField: 'screen_intake_code'
  },
  screenType: {
    param: 'screen_type',
    label: 'Screen type',
    type: 'select',
    textField: 'description',
    valueField: 'screen_type_code'
  },
  screenMaterial: {
    param: 'screen_material',
    label: 'Screen material',
    type: 'select',
    textField: 'description',
    valueField: 'screen_material_code'
  },
  otherScreenMaterial: {
    param: 'other_screen_material',
    label: 'Screen other material',
    type: 'text'
  },
  screenOpening: {
    param: 'screen_opening',
    label: 'Screen opening',
    type: 'select',
    textField: 'description',
    valueField: 'screen_opening_code'
  },
  screenBottom: {
    param: 'screen_bottom',
    label: 'Screen bottom',
    type: 'select',
    textField: 'description',
    valueField: 'screen_bottom_code'
  },
  screenInformation: {
    param: 'screen_information',
    label: 'Screen information',
    type: 'text'
  },
  filterPackRange: {
    param: 'filter_pack_range',
    label: 'Filter pack from/to',
    type: 'range'
  },
  filterPackMaterial: {
    param: 'filter_pack_material',
    label: 'Filter pack material',
    type: 'select',
    textField: 'description',
    valueField: 'filter_pack_material_code'
  },
  filterPackMaterialSize: {
    param: 'filter_pack_material_size',
    label: 'Filter pack material size',
    type: 'select',
    textField: 'description',
    valueField: 'filter_pack_material_size_code'
  },
  developmentMethods: {
    param: 'development_methods',
    label: 'Well development method',
    type: 'select',
    textField: 'description',
    valueField: 'development_method_code'
  },
  developmentHours: {
    param: 'development_hours',
    label: 'Development hours',
    type: 'range'
  },
  developmentNotes: {
    param: 'development_notes',
    label: 'Development notes',
    type: 'text'
  },
  yieldEstimationMethod: {
    param: 'yield_estimation_method',
    label: 'Yield estimation method',
    type: 'select',
    textField: 'description',
    valueField: 'yield_estimation_method_code'
  },
  yieldEstimationRate: {
    param: 'yield_estimation_rate',
    label: 'Yield estimation rate',
    type: 'range'
  },
  yieldEstimationDuration: {
    param: 'yield_estimation_duration',
    label: 'Yield estimation duration',
    type: 'range'
  },
  staticLevelBeforeTest: {
    param: 'static_level_before_test',
    label: 'SWL before test',
    type: 'range'
  },
  hydroFracturingPerformed: {
    param: 'hydro_fracturing_performed',
    label: 'Hydro-fracturing performed',
    type: 'radio',
    options: [{ text: 'Yes', value: 'true' }, { text: 'No', value: 'false' }]
  },
  hydroFracturingYieldIncrease: {
    param: 'hydro_fracturing_yield_increase',
    label: 'Increase in well yield',
    type: 'range'
  },
  drawdown: { param: 'drawdown', label: 'Drawdown', type: 'range' },
  recommendedPumpDepth: {
    param: 'recommended_pump_depth',
    label: 'Recommended pump depth',
    type: 'range'
  },
  recommendedPumpRate: {
    param: 'recommended_pump_rate',
    label: 'Recommended pump rate',
    type: 'range'
  },
  waterQualityCharacteristics: {
    param: 'water_quality_characteristics',
    label: 'Water quality characteristics',
    type: 'select',
    textField: 'description',
    valueField: 'code'
  },
  waterQualityColour: {
    param: 'water_quality_colour',
    label: 'Water quality colour',
    type: 'select',
    textField: 'description',
    valueField: 'code'
  },
  waterQualityOdor: {
    param: 'water_quality_odor',
    label: 'Water quality odor',
    type: 'text'
  },
  ems: {
    param: 'ems',
    label: 'EMS Id',
    type: 'booleanOrText'
  },
  finalCasingStickUp: {
    param: 'final_casing_stick_up',
    label: 'Final casing stick up',
    type: 'range'
  },
  bedrockDepth: {
    param: 'bedrock_depth',
    label: 'Depth to bedrock',
    type: 'range'
  },
  staticWaterLevel: {
    param: 'static_water_level',
    label: 'Static water level',
    type: 'range'
  },
  wellYield: {
    param: 'well_yield',
    label: 'Estimated well yield',
    type: 'range'
  },
  artesianFlow: {
    param: 'artesian_flow',
    label: 'Artesian flow',
    type: 'booleanOrRange'
  },
  artesianPressure: {
    param: 'artesian_pressure',
    label: 'Artesian pressure',
    type: 'booleanOrRange'
  },
  wellCapType: { param: 'well_cap_type', label: 'Well cap type', type: 'text' },
  wellDisinfected: {
    param: 'well_disinfected',
    label: 'Well disinfected',
    type: 'radio',
    options: [{ text: 'Yes', value: 'true' }, { text: 'No', value: 'false' }]
  },
  observationWellNumber: {
    param: 'observation_well_number',
    label: 'Observation well number',
    type: 'booleanOrText'
  },
  observationWellStatus: {
    param: 'observation_well_status',
    label: 'Observation well status',
    type: 'select',
    textField: 'description',
    valueField: 'obs_well_status_code'
  },
  finishedWellDepth: {
    param: 'finished_well_depth',
    label: 'Finished well depth - decommission',
    resultLabel: 'Finished well depth (feet)',
    type: 'range'
  },
  decommissionReason: {
    param: 'decommission_reason',
    label: 'Reason for well decommission',
    type: 'text'
  },
  decommissionMethod: {
    param: 'decommission_method',
    label: 'Decommission method',
    type: 'select',
    textField: 'description',
    valueField: 'decommission_method_code'
  },
  decommissionSealantMaterial: {
    param: 'decommission_sealant_material',
    label: 'Sealant material',
    type: 'text'
  },
  decommissionBackfillMaterial: {
    param: 'decommission_backfill_material',
    label: 'Backfill material',
    type: 'text'
  },
  decommissionDetails: {
    param: 'decommission_details',
    label: 'Decommission details',
    type: 'text'
  },
  comments: { param: 'comments', label: 'Comments', type: 'text' },
  alternativeSpecsSubmitted: {
    param: 'alternative_specs_submitted',
    label: 'Alt specs submitted',
    type: 'radio',
    options: [{ text: 'Yes', value: 'true' }, { text: 'No', value: 'false' }]
  },
  internalComments: {
    param: 'internal_comments',
    authenticated: true,
    label: 'Internal office comments',
    type: 'text'
  },
  aquiferLithology: {
    param: 'aquifer_lithology',
    label: 'Aquifer lithology',
    type: 'select',
    textField: 'description',
    valueField: 'aquifer_lithology_code'
  },
  aquiferVulnerabilityIndex: {
    param: 'aquifer_vulnerability_index',
    label: 'AVI',
    type: 'range'
  },
  storativity: { param: 'storativity', label: 'Storativity', type: 'range' },
  transmissivity: {
    param: 'transmissivity',
    label: 'Transmissivity',
    type: 'range'
  },
  hydraulicConductivity: {
    param: 'hydraulic_conductivity',
    label: 'Hydraulic Conductivity',
    type: 'text'
  },
  specificStorage: {
    param: 'specific_storage',
    label: 'Specific Storage',
    type: 'text'
  },
  specificYield: {
    param: 'specific_yield',
    label: 'Specific Yield',
    type: 'range'
  },
  testingMethod: {
    param: 'testing_method',
    label: 'Testing method',
    type: 'text'
  },
  testingDuration: {
    param: 'testing_duration',
    label: 'Testing duration',
    type: 'range'
  },
  analyticSolutionType: {
    param: 'analytic_solution_type',
    label: 'Analytic solution',
    type: 'range'
  },
  boundaryEffect: {
    param: 'boundary_effect',
    label: 'Boundary effect',
    type: 'range'
  },
  createUser: {
    authenticated: true,
    param: 'create_user',
    label: 'Created by',
    type: 'text'
  },
  createDate: {
    authenticated: true,
    param: 'create_date',
    label: 'Created date',
    type: 'dateRange'
  },
  updateUser: {
    authenticated: true,
    param: 'update_user',
    label: 'Updated by',
    type: 'text'
  },
  updateDate: {
    authenticated: true,
    param: 'update_date',
    label: 'Updated date',
    type: 'dateRange'
  },
  wellTagNumber: {
    param: 'well_tag_number',
    label: 'Well tag number',
    type: 'text'
  },
  identificationPlateNumber: {
    param: 'identification_plate_number',
    label: 'ID plate number',
    type: 'text'
  },
  streetAddress: {
    param: 'street_address',
    label: 'Street Address',
    type: 'text'
  },
  legalLot: {
    param: 'legal_lot',
    label: 'Legal lot',
    resultLabel: 'Lot',
    type: 'text'
  },
  legalPlan: {
    param: 'legal_plan',
    label: 'Legal plan',
    resultLabel: 'Plan',
    type: 'text'
  },
  legalDistrictLot: {
    param: 'legal_district_log',
    label: 'District lot',
    type: 'text'
  },
  legalPid: {
    param: 'legal_pid',
    label: 'PID',
    type: 'text'
  },
  diameter: {
    param: 'diameter',
    label: 'Diameter (inches)',
    type: 'range'
  },
  constructionStartDate: {
    param: 'construction_start_date',
    label: 'Construction start date',
    type: 'dateRange'
  },
  constructionEndDate: {
    param: 'construction_end_date',
    label: 'Construction end date',
    type: 'dateRange'
  },
  alterationStartDate: {
    param: 'alteration_start_date',
    label: 'Alteration start date',
    type: 'dateRange'
  },
  alterationEndDate: {
    param: 'alteration_end_date',
    label: 'Alteration end date',
    type: 'dateRange'
  },
  decomissionStartDate: {
    param: 'decomission_start_date',
    label: 'Decomission start date',
    type: 'dateRange'
  },
  decomissionEndDate: {
    param: 'decomission_end_date',
    label: 'Decomission end date',
    type: 'dateRange'
  }
}

const filterSections = {
  default: [
    {
      header: 'Search By',
      fields: [
        'matchAny',
        'well',
        'streetOrCity',
        'ownerName',
        'publicationStatus'
      ]
    },
    {
      header: 'Location',
      fields: [
        'legal',
        'landDistrict'
      ]
    },
    {
      header: 'Well Details',
      fields: [
        'wellStatus',
        'licencedStatus',
        'personResponsible',
        'orgResponsible',
        'dateOfWork',
        'wellDepth'
      ]
    },
    {
      header: 'Aquifer',
      fields: [
        'aquiferNr'
      ]
    }
  ],
  optional: [{
    header: 'Well Class',
    fields:
      ['wellClass',
        'wellSubclass',
        'intendedWaterUse',
        'wellIdPlateAttached',
        'idPlateAttachedBy',
        'waterSupplySystemName',
        'waterSupplyWellName']
  },
  {
    header: 'Person responsible for work',
    fields: ['drillerName', 'consultantName', 'consultantCompany']
  },
  {
    header: 'Well owner',
    authenticated: true,
    fields:
      ['ownerMailingAddress',
        'ownerCity',
        'ownerProvince',
        'ownerPostalCode']
  },
  {
    header: 'Well location',
    fields:
      ['legalBlock',
        'legalSection',
        'legalTownship',
        'legalRange',
        'locationDescription']
  },
  {
    header: 'Geocoordinates',
    fields: ['coordinateAcquisitionCode']
  },
  {
    header: 'Method of drilling',
    fields:
      ['groundElevation',
        'groundElevationMethod',
        'drillingMethods',
        'wellOrientation']
  },
  {
    header: 'Surface seal and backfill material',
    fields:
      ['surfaceSealMaterial',
        'surfaceSealDepth',
        'surfaceSealThickness',
        'surfaceSealMethod',
        'backfillAboveSurfaceSeal',
        'backfillDepth']
  },
  {
    header: 'Liner information',
    fields:
      ['linerMaterial',
        'linerDiameter',
        'linerThickness',
        'linerRange']
  },
  {
    header: 'Screen information',
    fields:
      ['screenIntakeMethod',
        'screenType',
        'screenMaterial',
        'otherScreenMaterial',
        'screenOpening',
        'screenBottom',
        'screenInformation']
  },
  {
    header: 'Filter pack',
    fields:
      ['filterPackRange',
        'filterPackMaterial',
        'filterPackMaterialSize']
  },
  {
    header: 'Well development',
    fields:
      ['developmentMethods', 'developmentHours', 'developmentNotes']
  },
  {
    header: 'Yield',
    fields:
      ['yieldEstimationMethod',
        'yieldEstimationRate',
        'yieldEstimationDuration',
        'staticLevelBeforeTest',
        'hydroFracturingPerformed',
        'hydroFracturingYieldIncrease',
        'drawdown',
        'recommendedPumpDepth',
        'recommendedPumpRate']
  },
  {
    header: 'Water quality',
    fields:
      ['waterQualityCharacteristics',
        'waterQualityColour',
        'waterQualityOdor',
        'ems']
  },
  {
    header: 'Well completion data',
    fields:
      ['finalCasingStickUp',
        'bedrockDepth',
        'staticWaterLevel',
        'wellYield',
        'artesianFlow',
        'artesianPressure',
        'wellCapType',
        'wellDisinfected']
  },
  {
    header: 'Observation well information',
    fields: ['observationWellNumber', 'observationWellStatus']
  },
  {
    header: 'Decommission',
    fields:
      ['finishedWellDepth',
        'decommissionReason',
        'decommissionMethod',
        'decommissionSealantMaterial',
        'decommissionBackfillMaterial',
        'decommissionDetails']
  },
  {
    header: 'Comments',
    fields:
      ['comments', 'alternativeSpecsSubmitted', 'internalComments']
  },
  {
    header: 'Well testing and aquifer details',
    fields:
      ['aquiferLithology',
        'aquiferVulnerabilityIndex',
        'storativity',
        'transmissivity',
        'hydraulicConductivity',
        'specificStorage',
        'specificYield',
        'testingMethod',
        'testingDuration',
        'analyticSolutionType',
        'boundaryEffect']
  },
  {
    header: 'Record maintenance',
    authenticated: true,
    fields: ['createUser', 'createDate', 'updateUser', 'updateDate']
  }]
}

const resultColumns = {
  default: [
    'wellTagNumber',
    'identificationPlateNumber',
    'ownerName',
    'streetAddress',
    'legalLot',
    'legalPlan',
    'legalDistrictLot',
    'landDistrict',
    'legalPid',
    'diameter',
    'finishedWellDepth'
  ],
  optional: [
    'publicationStatus',
    'wellStatus',
    'licencedStatus',
    'personResponsible',
    'orgResponsible',
    'wellDepth',
    'aquiferNr',
    'wellClass',
    'wellSubclass',
    'intendedWaterUse',
    'wellIdPlateAttached',
    'idPlateAttachedBy',
    'waterSupplySystemName',
    'waterSupplyWellName',
    'drillerName',
    'consultantName',
    'consultantCompany',
    'ownerMailingAddress',
    'ownerCity',
    'ownerProvince',
    'ownerPostalCode',
    'legalBlock',
    'legalSection',
    'legalTownship',
    'legalRange',
    'locationDescription',
    'coordinateAcquisitionCode',
    'groundElevation',
    'groundElevationMethod',
    'drillingMethods',
    'wellOrientation',
    'surfaceSealMaterial',
    'surfaceSealDepth',
    'surfaceSealThickness',
    'surfaceSealMethod',
    'backfillAboveSurfaceSeal',
    'backfillDepth',
    'linerMaterial',
    'linerDiameter',
    'linerThickness',
    'linerRange',
    'screenIntakeMethod',
    'screenType',
    'screenMaterial',
    'otherScreenMaterial',
    'screenOpening',
    'screenBottom',
    'screenInformation',
    'filterPackRange',
    'filterPackMaterial',
    'filterPackMaterialSize',
    'developmentMethods',
    'developmentHours',
    'developmentNotes',
    'yieldEstimationMethod',
    'yieldEstimationRate',
    'yieldEstimationDuration',
    'staticLevelBeforeTest',
    'hydroFracturingPerformed',
    'hydroFracturingYieldIncrease',
    'drawdown',
    'recommendedPumpDepth',
    'recommendedPumpRate',
    'waterQualityCharacteristics',
    'waterQualityColour',
    'waterQualityOdor',
    'ems',
    'finalCasingStickUp',
    'bedrockDepth',
    'staticWaterLevel',
    'wellYield',
    'artesianFlow',
    'artesianPressure',
    'wellCapType',
    'wellDisinfected',
    'observationWellNumber',
    'observationWellStatus',
    'decommissionReason',
    'decommissionMethod',
    'decommissionSealantMaterial',
    'decommissionBackfillMaterial',
    'decommissionDetails',
    'comments',
    'alternativeSpecsSubmitted',
    'internalComments',
    'aquiferLithology',
    'aquiferVulnerabilityIndex',
    'storativity',
    'transmissivity',
    'hydraulicConductivity',
    'specificStorage',
    'specificYield',
    'testingMethod',
    'testingDuration',
    'analyticSolutionType',
    'boundaryEffect',
    'createUser',
    'createDate',
    'updateUser',
    'updateDate',
    'constructionStartDate',
    'constructionEndDate',
    'alterationStartDate',
    'alterationEndDate',
    'decomissionStartDate',
    'decomissionEndDate'
  ]
}

export { searchFields, filterSections, resultColumns }
