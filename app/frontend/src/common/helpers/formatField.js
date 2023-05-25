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

// a map of difficult-to-read API field names to friendly descriptions
const fieldMap = {
  'lithologydescription_set': 'Lithology',
  'start': 'depth from',
  'end': 'depth to',
  'lithology_raw_data': 'raw_data',
  'lithology_colour': 'colour',
  'lithology_hardness': 'hardness',
  'lithology_moisture': 'moisture',
  'lithology_description': 'description',
  'lithology_observation': 'observations',
  'decommission_description_set': 'Decommission descriptions',
  'casing_set': 'Casings',
  'screen_set': 'Screens',
  'linerperforation_set': 'Liner perforations'
}

/**
 * Formats an API field name into a readable description (using fieldMap), or if the key
 * isn't present in fieldMap, returns the original key.
 *
 * @param {string} key - an API field key to format
 * @return {string} returns either the friendly description (if in fieldMap) or the original key
 */
const formatField = (key) => {
  return fieldMap[key] || key
}

export default formatField
