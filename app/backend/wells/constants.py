MAX_EXPORT_COUNT = 999999
MAX_LOCATION_COUNT = 999999

WELL_TAGS_PUBLIC = [
  { "text": "Well Construction Report", "value": "Well Construction" },
  { "text": "Well Alteration Report", "value":  "Well Alteration" },
  { "text": "Well Decommission Report", "value":  "Well Decommission" },
  { "text": "Pictures/Photos", "value":  "Photo" },
  { "text": "Well Pump Installation Report", "value":  "Well Pump Installation" },
  { "text": "Pumping Test Raw Data", "value":  "Pumping Test Data" },
  { "text": "Directions Artesian Conditions", "value": "Directions Artesian Conditions"},
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
