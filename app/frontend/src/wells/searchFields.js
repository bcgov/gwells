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
        { id: 'personResponsible', param: 'person_responsible', label: 'Person responsible for work', type: 'select', textField: 'name', valueField: 'driller_guid' },
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
        { id: 'waterSupplyWellName', param: 'water_supply_system_well_name', label: 'Water supply well name', type: 'text' }
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
        { id: 'linerFrom', param: 'liner_from', label: 'Liner from', type: 'range' },
        { id: 'linerTo', param: 'liner_to', label: 'Liner to', type: 'range' }
      ]
    },
    {
      header: 'Screen information',
      fields: [
        { id: 'screenIntakeMethod', param: 'screen_intake_method', label: 'Screen intake', type: 'select', textField: 'description', valueField: 'screen_intake_code' }
      ]
    }
  ]
}

export default searchFields
