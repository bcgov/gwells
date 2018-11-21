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

package pages

class RegistryPage extends BaseAppPage {
  static at = { pageTitle.text() == 'Register of Well Drillers and Well Pump Installers' }
  static url = 'registries'
  static content = {
    pageTitle { $('main h4') }

    bodyContent { $('#main-content .card-body') }

    addNewEntryButton(required:false) { $('#addNewEntryButton') }
    manageCompaniesButton(required:false) { $('#manageCompaniesButton') }

    registrationStatusDropdown(required:false) { $('#manageCompaniesButton') }

    wellDrillerRadioButton { $('#activityDriller') }
    wellPumpInstallerRadioButton { $('#activityInstaller') }

    individualOrCompanyOrRegistrationSearchField { $('#regTypeInput') }

    searchButton { $('#personSearchSubmit') }

    searchResultsTable(required:false) { $('#registry-table') }
  }

  void clickAddNewEntryButton() {
    waitFor { addNewEntryButton.click() }
  }

  void clickManageCompaniesButton() {
    waitFor { manageCompaniesButton.click() }
  }

  void clickSearchButton() {
    searchButton.click()
  }

  void clickWellDrillerRadioButton() {
    wellDrillerRadioButton.parent().click()
  }

  void clickWellPumpInstallerRadioButton() {
    wellPumpInstallerRadioButton.parent().click()
  }

  void setIndividualOrCompanyOrRegistrationSearchField(String value) {
    individualOrCompanyOrRegistrationSearchField.value(value)
  }

  Boolean foundSearchResults() {
    waitFor { searchResultsTable.$('tbody tr').size() != 0 }
  }
}
