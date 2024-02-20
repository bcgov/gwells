// Aquifer 1143 is the uncorrelated wells aquifer
// See task:  https, value, //apps.nrs.gov.bc.ca/int/jira/browse/WATER-999 for more information
export const AQUIFER_ID_FOR_UNCORRELATED_WELLS = 1143

// See task: https, value, //apps.nrs.gov.bc.ca/int/jira/browse/WATER-1775
export const MAX_API_RESULT_AND_EXPORT_COUNT = 999999

export const WELL_TAGS_PUBLIC = [
  { text: "Directions Artesian Conditions", value: "Directions_ArtesianConditions"},
  { text: "Map(s)", value:  "Map" },
  { text: "Pictures/Photos", value:  "Photo" },
  { text: "Pumping Test Raw Data", value:  "Pumping Test Data" },
  { text: "Well Alteration Report", value:  "Well Alteration" },
  { text: "Well Construction Report", value: "Well Construction" },
  { text: "Well Decommission Report", value:  "Well Decommission" },
  { text: "Well Pump Installation Report", value:  "Well Pump Installation" },
  { text: "Other", value:  "Additional Details" },
].sort((a,b) => {
  if(a.text === 'Other') return 1;
  if(b.text === 'Other') return -1;
  return a.text.toLowerCase().localeCompare(b.text.toLowerCase())
})

export const WELL_TAGS_PRIVATE = [
  { text: "Alternative Specifications", value:  "Alternative Specs" },
  { text: "Artesian Management Report", value:  "ArtesianMgmtReport" },
  { text: "Consultant's Report", value:  "Consultants Report" },
  { text: "Health Authority Report", value:  "Health Authority" },
  { text: "Pumping Test Info", value:  "Pumping Test Info" },
  { text: "Signed Sharing Agreement", value:  "Sharing Agreement" },
  { text: "Water Quality Report", value:  "Water Quality" },
  { text: "Well Inspection Report", value:  "Well Inspection" },
].sort((a,b) => a.text.toLowerCase().localeCompare(b.text.toLowerCase()))

export const WELL_TAGS = [
  {
    text: "Select Document Type",
    value: null,
  },
  {
    label: "Public Document",
    options: WELL_TAGS_PUBLIC,
  },
  {
    label: "Private Document",
    options: WELL_TAGS_PRIVATE,
  },
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
    analysis_method: 'Mathematical solutions (Theis, Cooper-Jacob, Neuman, etc.) where response data (discharge, drawdown/time) from pumping tests are used to estimate the hydraulic properties of aquifers.',
  },
  location_vue: {
    legal_description_fields: 'Enter as many fields as possible. Additional information that does not fit should go in "Description of Well Location."',
  }
}

export const TYPE_OF_WORK = {
  CON: "CON",
  ALT: "ALT",
  DEC: "DEC",
}

export const WELL_CLASS = {
  DEWATERING_DRAINAGE: "DEW_DRA",
  WATER_SUPPLY: "WATR_SPPLY",
  INJECTION: "INJECTION",
  RECHARGE: "RECHARGE",
}

export const WELL_SUBCLASS = {
  PERMANENT: "46300f40-fc6b-4c77-a58e-74472cd69f5d",
}

export const WELL_SUBMISSION_STRINGS = {
  START_DATE_OF_WORK: "Start Date of Work",
  END_DATE_OF_WORK: "End Date of Work",
  WELL_IDENTIFICATION_PLATE_NUMBER: "Well Identification Plate Number",
  WELL_IDENTIFICATION_PLATE_ATTACHED: "Where Identification Plate Attached",
  TOTAL_DEPTH_DRILLED: "Total Depth Drilled",
  FINISHED_WELL_DEPTH: "Finished Well Depth",
  DRILLING_METHODS: "Drilling Method(s)",
}

export const MANDATORY_WELL_SUBMISSION_STRINGS = {
  START_DATE_OF_WORK: "Start Date of Work *",
  END_DATE_OF_WORK: "End Date of Work *",
  WELL_IDENTIFICATION_PLATE_NUMBER: "Well Identification Plate Number *",
  WELL_IDENTIFICATION_PLATE_ATTACHED: "Where Identification Plate Attached *",
  TOTAL_DEPTH_DRILLED: "Total Depth Drilled *",
  FINISHED_WELL_DEPTH: "Finished Well Depth *",
  DRILLING_METHODS: "Drilling Method(s) *",
}

export const NEW_WELL_CONSTRUCTION_VALIDATION_DATE = '2024-01-01'

export const DATE_INPUT_TYPE = {
  START_DATE: 'workStartDate',
  END_DATE: 'workEndDate'
}
