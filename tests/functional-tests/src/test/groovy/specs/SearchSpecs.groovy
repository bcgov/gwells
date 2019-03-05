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

package specs

import pages.HomePage

import spock.lang.Title
import spock.lang.Narrative

@Title('Groundwater Wells Search Tests')
@Narrative('''As a public user, I want to search for existing wells.''')
class SearchSpecs extends BaseSpec {

  void setup() {
    to HomePage
  }

  void 'Search by "Well Tag Number or Well Identification Plate Number" field'() {
    given: 'I populate the "Well Tag Number or Well Identification Plate Number" field'
      setWellTagOrIdentificationPlateNumber(123)
    when: 'I click the Search button'
      clickSearchButton()
    then: 'The search is executed and a table containing at least 1 matching result is displayed'
      getSearchResultsCount() != 0
  }

  void 'Search by "Street Address" field'() {
    given: 'I populate the "Street Address" field'
      setStreetAddress('anahim')
    when: 'I click the Search button'
      clickSearchButton()
    then: 'The search is executed and a table containing at least 1 matching result is displayed'
      getSearchResultsCount() != 0
  }

  void 'Search by "Legal Plan or District Lot or Parcel Identification Number PID" field'() {
    given: 'I populate the "Legal Plan or District Lot or Parcel Identification Number PID" field'
      setLegalPlanOrDistrictLotorPID('405')
    when: 'I click the Search button'
      clickSearchButton()
    then: 'The search is executed and a table containing at least 1 matching result is displayed'
      getSearchResultsCount() != 0
  }

  void 'Search by "Owner Name" field'() {
    given: 'I populate the "Owner Name" field'
      setOwnerName('police')
    when: 'I click the Search button'
      clickSearchButton()
    then: 'The search is executed and a table containing at least 1 matching result is displayed'
      getSearchResultsCount() != 0
  }
}
