// Aquifer 1143 is the uncorrelated wells aquifer
// See task:  https, value, //apps.nrs.gov.bc.ca/int/jira/browse/WATER-999 for more information
export const AQUIFER_ID_FOR_UNCORRELATED_WELLS = 1143

// See task: https, value, //apps.nrs.gov.bc.ca/int/jira/browse/WATER-1775
export const MAX_API_RESULT_AND_EXPORT_COUNT = 999999

export const WELL_TAGS_PUBLIC = [
  { text: "Directions Artesian Conditions", value: "Directions Artesian Conditions"},
  { text: "Map(s)", value:  "Map" },
  { text: "Pictures/Photos", value:  "Photo" },
  { text: "Pumping Test Raw Data", value:  "Pumping Test Data" },
  { text: "Well Alteration Report", value:  "Well Alteration" },
  { text: "Well Construction Report", value: "Well Construction" },
  { text: "Well Decommission Report", value:  "Well Decommission" },
  { text: "Well Pump Installation Report", value:  "Well Pump Installation" },
  { text: "Other", value:  "Additional Details" },
]

export const WELL_TAGS_PRIVATE = [
  { text: "Alternative Specifications", value:  "Alternative Specs" },
  { text: "Artesian Management Report", value:  "ArtesianMgmtReport" },
  { text: "Consultant's Report", value:  "Consultants Report" },
  { text: "Health Authority Report", value:  "Health Authority" },
  { text: "Pumping Test Info", value:  "Pumping Test Info" },
  { text: "Signed Sharing Agreement", value:  "Sharing Agreement" },
  { text: "Water Quality Report", value:  "Water Quality" },
  { text: "Well Inspection Report", value:  "Well Inspection" },
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
