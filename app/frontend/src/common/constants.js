// Aquifer 1143 is the uncorrelated wells aquifer
// See task:  https, value, //apps.nrs.gov.bc.ca/int/jira/browse/WATER-999 for more information
export const AQUIFER_ID_FOR_UNCORRELATED_WELLS = 1143

// See task: https, value, //apps.nrs.gov.bc.ca/int/jira/browse/WATER-1775
export const MAX_API_RESULT_AND_EXPORT_COUNT = 999999

export const WELL_TAGS_PUBLIC = [
  { text:  "Well Construction Report", value: "Well Construction" },
  { text:  "Well Alteration Report", value:  "Well Alteration" },
  { text: "Well Decommission Report", value:  "Well Decommission" },
  { text: "Pictures/Photos", value:  "Photo" },
  { text: "Well Pump Installation Report", value:  "Well Pump Installation" },
  { text: "Pumping Test Report", value:  "Pumping Test" },
  { text: "Map(s)", value:  "Map" },
  { text: "Other", value:  "Additional Well Details" },
]

export const WELL_TAGS_PRIVATE = [
  { text: "Well Inspection Report", value:  "Well Inspection" },
  { text: "Confirmation/Alternative Specifications", value:  "Alternative Specs" },
  { text: "Water Quality Report", value:  "Water Quality" },
  { text: "Health Authority Report", value:  "Health Authority" },
  { text: "Consultant's Report", value:  "Consultants Report" },
]

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
