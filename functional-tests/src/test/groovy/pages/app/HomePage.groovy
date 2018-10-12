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

class HomePage extends BaseAppPage {
  static at = { pageTitle.text() == 'Groundwater Well Search' }
  static url = ''
  static content = {
    pageTitle { $('#main-content h2') }

    bodyContent { $('#main-content') }

    wellTagOrPlateField { $('#id_well') }
    streetAddressField { $('#id_addr') }
    legalPlanOrDistrictLotOrPIDField { $('#id_legal') }
    ownerNameField { $('#id_owner') }

    searchButton { $('input', type:'submit', value:'Search') }

    searchResultsTable(required:false) { $('#results') }
  }

  void setWellTagOrIdentificationPlateNumber(int value) {
    wellTagOrPlateField.value(value)
  }

  void setStreetAddress(String address) {
    streetAddressField.value(address)
  }

  void setLegalPlanOrDistrictLotorPID(String value) {
    legalPlanOrDistrictLotOrPIDField.value(value)
  }

  void setOwnerName(String name) {
    ownerNameField.value(name)
  }

  void clickSearchButton() {
    searchButton.click()
  }

  Boolean foundSearchResults() {
    waitFor { searchResultsTable.$('tbody tr').size() != 0 }
  }
}
