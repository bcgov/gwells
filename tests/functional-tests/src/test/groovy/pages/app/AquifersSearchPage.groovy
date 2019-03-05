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

class AquifersSearchPage extends BaseAppPage {
  static at = { pageTitle.text() == 'Aquifer Search' }
  static url = 'aquifers'
  static content = {
    pageTitle { $('main h4') }

    nameField { $('#aquifers-name') }
    numberField { $('#aquifers-number') }

    searchButton { $('#aquifers-search') }

    searchResultsTable(required:false) { $('#aquifers-results') }
  }

  void setAquiferName(String name) {
    nameField.value(name)
  }

  void setAquiferNumber(int number) {
    numberField.value(number)
  }

  void clickSearchButton() {
    searchButton.click()
  }

  int getSearchResultsCount() {
    waitFor { searchResultsTable.$('tbody tr').hasNot(".b-table-empty-row").size() }
  }

  void clickFirstSearchResult() {
    // click the first column with an anchor tag, from the first row of the search results table
    waitFor { searchResultsTable.$('tbody tr')[0].$('td a')[0].click() }
  }
}
