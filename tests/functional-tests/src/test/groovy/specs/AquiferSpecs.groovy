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

import pages.AquifersSearchPage
import pages.AquiferAddPage
import pages.AquiferEditPage
import pages.AquiferSummaryPage
import pages.ConfirmSaveModal

import spock.lang.Title
import spock.lang.Narrative
import spock.lang.Shared
import spock.lang.Ignore

@Title('Groundwater Wells Aquifer Tests')
@Narrative('''As a user, I want to create, search for, and edit aquifers.''')
class AquiferSpecs extends LoggedInSpec {

  @Shared
  String aquifersName

  @Shared
  String aquifersNumber

  void 'Add a new aquifer'() {
    given: 'I am logged in as an admin user'
      logInAsAdminUser()
      to AquiferAddPage
    and: 'I populate all required fields for a new aquifer'
      aquifersName = makeUnique('BDDAquiferName')
      setName(aquifersName)
      setLocationDescription('40 km West of East')
      setMaterial('Sand')
      setQualityConcern('Local')
      setSize(1234.5)
      setKnownWaterUse('Multiple')
      setComment('Add new aquifer')
      setYearOfMapping(2018)
      setLithoStratigraphicUnit('Jurassic')
      setVulnerability('High')
      setSubtype('2 - Unconfined sand and gravel - deltaic')
      setProductivity('Low')
      setDemand('Moderate')
    when: 'I click the "Save" button'
      clickSaveButton()
      page(ConfirmSaveModal)
      confirmSave()
      // In order to capture the aquifer number, we need to be on the AquiferSummaryPage.
      // But we can't do that in the 'then' block as only assertions are allowed, not assignments.
      at new AquiferSummaryPage(aquifersName)
      aquifersNumber = getAquiferNumber()
    then: 'The aquifer is created and I am taken to the aquifer summary page'
      at new AquiferSummaryPage(aquifersName)
  }

  void 'Search by "Aquifer name" field'() {
    given: 'I populate the "Aquifer name" field'
      to AquifersSearchPage
      setAquiferName(aquifersName)
    when: 'I click the Search button'
      clickSearchButton()
    then: 'The search is executed and a table containing at least 1 matching result is displayed'
      getSearchResultsCount() != 0
  }

  @Ignore
  void 'Search by "Aquifer number" field'() {
    given: 'I populate the "Aquifer number" field'
      to AquifersSearchPage
      setAquiferNumber(aquifersNumber)
    when: 'I click the Search button'
      clickSearchButton()
    then: 'The search is executed and a table containing at least 1 matching result is displayed'
      getSearchResultsCount() != 0
  }

  @Ignore
  void 'Edit an existing aquifer'() {
    given: 'I am logged in as an admin user'
      logInAsAdminUser()
      to AquifersSearchPage
    and: 'I select an aquifer from the search results'
      setAquiferName(aquifersName)
      setAquiferNumber(aquifersNumber)
      clickSearchButton()
      clickFirstSearchResult()
      at new AquiferSummaryPage(aquifersName, aquifersNumber)
    and: 'I click the edit button'
      clickEditButton()
      at new AquiferEditPage(aquifersName, aquifersNumber)
    and: 'I update all fields of the existing aquifer'
      setName("${aquifersName}Edit")
      setLocationDescription('41 km East of West')
      setMaterial('Bedrock')
      setQualityConcern('None')
      setSize(5432.1)
      setKnownWaterUse('Domestic')
      setComment('Edit existing aquifer')
      setYearOfMapping(2017)
      setLithoStratigraphicUnit('Cretaceous')
      setVulnerability('Low')
      setSubtype('5b - Karstic limestone')
      setProductivity('High')
      setDemand('High')
    when: 'I click the "Save" button'
      clickSaveButton()
      page(ConfirmSaveModal)
      confirmSave()
    then: 'The aquifer is updated and I am taken to the aquifer summary page'
      at new AquiferSummaryPage("${aquifersName}Edit", aquifersNumber)
    and: 'A success alert is displayed'
      editAquiferSuccessAlertDisplayed()
  }
}
