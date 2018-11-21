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

import pages.AquifersPage

import spock.lang.Title
import spock.lang.Narrative

@Title('Groundwater Well Aquifer Search Tests')
@Narrative('''As a public user, I want to search for existing aquifers.''')
class AquiferSearchSpecs extends BaseSpec {

  void setup() {
    to AquifersPage
  }

  void 'Search by "Aquifer name" field'() {
    given: 'I populate the "Aquifer name" field'
      setAquiferName('a')
    when: 'I click the Search button'
      clickSearchButton()
    then: 'The search is executed and a table containing at least 1 matching result is displayed'
      foundSearchResults()
  }

  void 'Search by "Aquifer number" field'() {
    given: 'I populate the "Aquifer number" field'
      setAquiferNumber(123)
    when: 'I click the Search button'
      clickSearchButton()
    then: 'The search is executed and a table containing at least 1 matching result is displayed'
      foundSearchResults()
  }
}
