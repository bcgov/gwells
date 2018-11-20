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

import pages.RegistryPage

import spock.lang.Title
import spock.lang.Narrative

@Title('Groundwater Well Registry Tests')
@Narrative('''As a user, I want to search the registry of well operators.''')
class RegistrySpecs extends LoggedInSpec {

  void 'Search for Well Drillers as a public user'() {
    given: 'I am a public user on the Registry page'
      to RegistryPage
    and: 'I select the "Well Driller" profession type'
      clickWellDrillerRadioButton()
    when: 'I click the Search button'
      clickSearchButton()
    then: 'The search is executed and a table containing at least 1 matching result is displayed'
      foundSearchResults()
  }

  void 'Search for Well Pump Installers as a public user'() {
    given: 'I am a public user on the Registry page'
      to RegistryPage
    and: 'I select the "Well Pump Installer" profession type'
      clickWellPumpInstallerRadioButton()
    when: 'I click the Search button'
      clickSearchButton()
    then: 'The search is executed and a table containing at least 1 matching result is displayed'
      foundSearchResults()
  }

  void 'Search using "Individual, company, or registration number" field as a public user'() {
    given: 'I am a public user on the Registry page'
      to RegistryPage
    and: 'I set the search keywords'
      setIndividualOrCompanyOrRegistrationSearchField('a')
    when: 'I click the Search button'
      clickSearchButton()
    then: 'The search is executed and a table containing at least 1 matching result is displayed'
      foundSearchResults()
  }
}
