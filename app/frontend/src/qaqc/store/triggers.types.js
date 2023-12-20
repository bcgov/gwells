/**
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

// the QUERY trigger means the search was triggered by a querystring in the URL
// e.g. the user bookmarked a search or shared a link.
export const QUERY_TRIGGER = 'QUERY_TRIGGER'

// the search trigger means the basic or advanced search form was used to search for wells.
export const SEARCH_TRIGGER = 'SEARCH_TRIGGER'

// the filter trigger means that the search was triggered via search result filters.
export const FILTER_TRIGGER = 'FILTER_TRIGGER'
