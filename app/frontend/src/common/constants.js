// Aquifer 1143 is the uncorrelated wells aquifer
// See task:  https, value, //apps.nrs.gov.bc.ca/int/jira/browse/WATER-999 for more information
export const AQUIFER_ID_FOR_UNCORRELATED_WELLS = 1143

// See task: https, value, //apps.nrs.gov.bc.ca/int/jira/browse/WATER-1775
export const MAX_API_RESULT_AND_EXPORT_COUNT = 999999

export const WELL_TAGS_PUBLIC = [
  { text: 'Directions Artesian Conditions', value: 'Directions_ArtesianConditions' },
  { text: 'Map(s)', value: 'Map' },
  { text: 'Pictures/Photos', value: 'Photo' },
  { text: 'Pumping Test Raw Data', value: 'Pumping Test Data' },
  { text: 'Well Alteration Report', value: 'Well Alteration' },
  { text: 'Well Construction Report', value: 'Well Construction' },
  { text: 'Well Decommission Report', value: 'Well Decommission' },
  { text: 'Well Pump Installation Report', value: 'Well Pump Installation' },
  { text: 'Other', value: 'Additional Details' }
].sort((a, b) => {
  if (a.text === 'Other') return 1
  if (b.text === 'Other') return -1
  return a.text.toLowerCase().localeCompare(b.text.toLowerCase())
})

export const WELL_TAGS_PRIVATE = [
  { text: 'Alternative Specifications', value: 'Alternative Specs' },
  { text: 'Artesian Management Report', value: 'ArtesianMgmtReport' },
  { text: "Consultant's Report", value: 'Consultants Report' },
  { text: 'Health Authority Report', value: 'Health Authority' },
  { text: 'Pumping Test Info', value: 'Pumping Test Info' },
  { text: 'Signed Sharing Agreement', value: 'Sharing Agreement' },
  { text: 'Water Quality Report', value: 'Water Quality' },
  { text: 'Well Inspection Report', value: 'Well Inspection' }
].sort((a, b) => a.text.toLowerCase().localeCompare(b.text.toLowerCase()))

export const WELL_TAGS = [
  {
    text: 'Select Document Type',
    value: null
  },
  {
    label: 'Public Document',
    options: WELL_TAGS_PUBLIC
  },
  {
    label: 'Private Document',
    options: WELL_TAGS_PRIVATE
  }
]

export const TOOLTIP_TEXT = {
  pumping_test_information: {
    pumping_test: 'Describes the type of test (step, recovery, constant rate pumping test) and type of well (pumping well, observation well).',
    boundary_effect: 'Describe the specific conditions that are to be imposed at the boundaries of a groundwater flow region such as a recharge (river, lake) boundary or a barrier (impermeable rock) boundary where the assumption that the aquifer is of infinite extent is no longer valid.',
    storativity: 'Storativity (S) is a dimensionless measure of the volume of water that will be discharged from an aquifer per unit area of the aquifer and per unit reduction in hydraulic head.',
    transmissivity: 'Describes the ability of the aquifer to transmit groundwater throughout its entire saturated thickness, is measured as the rate at which groundwater can flow through an aquifer section of unit width under a unit hydraulic gradient.',
    hydraulic_conductivity: 'A measure of how easily water can pass through soil or rock.',
    specific_yield: 'The quantity of water that a unit volume of saturated permeable rock or soil will yield when drained by gravity.',
    specific_capacity: 'The specific capacity of a well is simply the pumping rate (yield) divided by the drawdown.',
    analysis_method: 'Mathematical solutions (Theis, Cooper-Jacob, Neuman, etc.) where response data (discharge, drawdown/time) from pumping tests are used to estimate the hydraulic properties of aquifers.'
  },
  location_vue: {
    legal_description_fields: 'Enter as many fields as possible. Additional information that does not fit should go in "Description of Well Location."'
  },
  qaqc_table: {
    diameterNull: 'Diameter in the last line of the Casing Details table on the Well Summary page. It is used to check if the casing information is missing',
    aquiferLithologyNull: 'Raw Data in the last line of the Lithology table on the Well Summary page; It is used to check if lithology information is missing',
    wellActivityType: 'Activity in the Well Activity table on the Well Summary page',
    workStartDateNull: 'Work Start Date in the Well Activity Table on the Well Summary page',
    workEndDateNull: 'Work End Date in the Well Activity Table on the Well Summary page',
    createDate: 'When the well record was entered/created in UTC time',
    geocodeDistance: 'The distance from well to location determined by the BC Address Geocoder API.',
    distanceToPid: 'The distance from well to BC Parcel Fabric Polygon with matching Parcel Identifier (PID). A higher value indicates higher probability of a location error. NULL indicates no matching PID found.',
    scoreAddress: 'Token Set Ratio score for matching wells address to reverse geocoded address (street number/name/direction). A lower score indicates a higher probability of a location error.',
    scoreCity: 'Token Set Ratio score for matching wells city to reverse geocoded locality. A lower score indicates a higher probability of a location error.'
  },
  aquifer_details: {
    vulnerabilityInfo: 'The susceptibility of an aquifer to contamination from surface sources. Three vulnerability categories are used: high, moderate, or low. Vulnerability is based on hydrogeology alone and does not consider the existing type of land use or nature of the potential contaminants.',
    aquiferSubtype: `There are different types of aquifers, depending on the geologic materials in which they occur. Subtype descriptions can be <a href='https://www2.gov.bc.ca/gov/content/environment/air-land-water/water/groundwater-wells-aquifers/understanding-aquifers/aquifer-subtype-code-description' target='_blank' rel='noopener noreferrer' class='d-print-url'>found here</a>.`,
    aquiferQualityConcerns: `Classified as unknown/none, isolated, local, or regional. For details see page 16 of the Guide to Using the <a href='https://www2.gov.bc.ca/assets/gov/environment/air-land-water/water/science-data/aquifer_maps_guide.pdf' target='_blank' rel='noopener noreferrer' class='d-print-url'>BC Aquifer Classification System</a>.`,
    productivityInfo: 'Productivity describes the rate of groundwater flow from wells and springs and the abundance of groundwater in an aquifer. Classified as low, medium, or high.',
    calculatedDemandDensity: 'Calculated based on the number of wells known to be completed in the aquifer per square kilometer. Light ≤ 4 km²; Medium 4 – 20 km²; Heavy > 20 km²',
    correlatedWellsCount: 'The total number of wells that fall within the aquifer boundaries and, based on depth and lithology, are believed to withdraw water from that aquifer.',
    uncorrelatedWellsCount: 'The total number of wells that fall within the aquifer polygon but have not been correlated to any aquifer. These wells may potentially be located within this aquifer or may be completed within an aquitard or within another aquifer located at a different depth.',
    artesianWells: 'A flowing artesian well is one that has been drilled into an aquifer where the pressure within the aquifer forces the groundwater to rise above the land surface naturally without using a pump.',
    aquiferAdvancedMapping: 'Aquifers with advanced mapping have been mapped in three dimensions. Generally, cross-sections and/or three-dimensional models, have been developed.',
    aquiferObservationWells: 'Groundwater Observation Wells are used to monitor aquifer groundwater levels and chemistry over time.',
    aquiferWaterQualityInformation: 'Indicates there are wells correlated to the aquifer with water quality information in the Environmental Monitoring Data System (EnMoDS) database.',
    aquiferConnectedInfo: 'Likelihood of hydraulic connection between groundwater and surface water requires aquifer specific assessment and professional judgement.',
    aquiferNumericalModel: 'Numerical groundwater flow models are mathematical representations of groundwater flow in an aquifer and the interactions with adjacent surface water bodies.',
    aquiferWaterBudget: 'Water budget studies are an accounting of all the water flowing into and out of an aquifer and/or a watershed over a specified time.',
    aquiferGroundwaterSurfaceInteractions: 'Studies that characterize the exchange of water and/or chemicals between the land surface and the subsurface.',
    aquiferArtesianAdvisory: 'Advisories highlighting regional concerns about water availability, water quality, and flowing artesian conditions.',
    aquiferNotations: `Water allocation notations are a water management tool that indicates a potential lack of water availability/quality in a source. For details click <a href='https://www2.gov.bc.ca/gov/content/environment/air-land-water/water/water-licensing-rights/water-allocation-notations'>here</a>.`
  }
}

export const TYPE_OF_WORK = {
  CON: 'CON',
  ALT: 'ALT',
  DEC: 'DEC'
}

export const WELL_CLASS = {
  DEWATERING_DRAINAGE: 'DEW_DRA',
  WATER_SUPPLY: 'WATR_SPPLY',
  INJECTION: 'INJECTION',
  RECHARGE: 'RECHARGE'
}

export const WELL_SUBCLASS = {
  PERMANENT: '46300f40-fc6b-4c77-a58e-74472cd69f5d'
}

export const WELL_SUBMISSION_STRINGS = {
  START_DATE_OF_WORK: 'Start Date of Work',
  END_DATE_OF_WORK: 'End Date of Work',
  WELL_IDENTIFICATION_PLATE_NUMBER: 'Well Identification Plate Number',
  WELL_IDENTIFICATION_PLATE_ATTACHED: 'Where Identification Plate Attached',
  TOTAL_DEPTH_DRILLED: 'Total Depth Drilled',
  FINISHED_WELL_DEPTH: 'Finished Well Depth',
  DRILLING_METHODS: 'Drilling Method(s)'
}

export const MANDATORY_WELL_SUBMISSION_STRINGS = {
  START_DATE_OF_WORK: 'Start Date of Work *',
  END_DATE_OF_WORK: 'End Date of Work *',
  WELL_IDENTIFICATION_PLATE_NUMBER: 'Well Identification Plate Number *',
  WELL_IDENTIFICATION_PLATE_ATTACHED: 'Where Identification Plate Attached *',
  TOTAL_DEPTH_DRILLED: 'Total Depth Drilled *',
  FINISHED_WELL_DEPTH: 'Finished Well Depth *',
  DRILLING_METHODS: 'Drilling Method(s) *'
}

export const NEW_WELL_CONSTRUCTION_VALIDATION_DATE = '2024-01-01'

export const DATE_INPUT_TYPE = {
  START_DATE: 'workStartDate',
  END_DATE: 'workEndDate'
}
