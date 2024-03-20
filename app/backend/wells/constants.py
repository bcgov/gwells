MAX_EXPORT_COUNT = 999999
MAX_LOCATION_COUNT = 999999

WELL_TAGS_PUBLIC = [
  { "text": "Well Construction Report", "value": "Well Construction" },
  { "text": "Well Alteration Report", "value":  "Well Alteration" },
  { "text": "Well Decommission Report", "value":  "Well Decommission" },
  { "text": "Pictures/Photos", "value":  "Photo" },
  { "text": "Well Pump Installation Report", "value":  "Well Pump Installation" },
  { "text": "Pumping Test Raw Data", "value":  "Pumping Test Data" },
  { "text": "Directions Artesian Conditions", "value": "Directions_ArtesianConditions"},
  { "text": "Map(s)", "value":  "Map" },
  { "text": "Other", "value":  "Additional Details" },
]


WELL_TAGS_PRIVATE = [
  { "text": "Well Inspection Report", "value":  "Well Inspection" },
  { "text": "Alternative Specifications", "value":  "Alternative Specs" },
  { "text": "Water Quality Report", "value":  "Water Quality" },
  { "text": "Health Authority Report", "value":  "Health Authority" },
  { "text": "Consultant's Report", "value":  "Consultants Report" },
  { "text": "Signed Sharing Agreement", "value":  "Sharing Agreement" },
  { "text": "Artesian Management Report", "value":  "ArtesianMgmtReport" },
  { "text": "Pumping Test Info", "value":  "Pumping Test Info" },
]

WELL_TAGS = []
WELL_TAGS.extend(WELL_TAGS_PUBLIC.copy())
WELL_TAGS.extend(WELL_TAGS_PRIVATE.copy())

# bc geocoder endpoint of interest
GEOCODER_ENDPOINT = "https://geocoder.api.gov.bc.ca/sites/nearest.json"
ADDRESS_COLUMNS = [
    "fullAddress",
    "siteName",
    "unitDesignator",
    "unitNumber",
    "unitNumberSuffix",
    "civicNumber",
    "civicNumberSuffix",
    "streetName",
    "streetType",
    "isStreetTypePrefix",
    "streetDirection",
    "isStreetDirectionPrefix",
    "streetQualifier",
    "localityName",
    "localityType",
    "electoralArea",
    "provinceCode",
    "locationPositionalAccuracy",
    "locationDescriptor",
    "siteID",
    "blockID",
    "fullSiteDescriptor",
    "accessNotes",
    "siteStatus",
    "siteRetireDate",
    "changeDate",
    "isOfficial",
    "distance",
]

WELL_ACTIVITY_CODE_CONSTRUCTION = 'CON'
WELL_ACTIVITY_CODE_DECOMMISSION = 'DEC'
WELL_ACTIVITY_CODE_ALTERATION = 'ALT'
WELL_ACTIVITY_CODE_STAFF_EDIT = 'STAFF_EDIT'