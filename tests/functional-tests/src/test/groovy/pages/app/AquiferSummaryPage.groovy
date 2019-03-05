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

class AquiferSummaryPage extends BaseAppPage {
  static at = {
    browser.getCurrentUrl() =~ /aquifers\/\d+$/ &&
    pageTitle.text() == 'Aquifer Summary' &&
    nameField().text() == aquiferName &&
    numberField.text() == getAquiferNumber()
  }
  static content = {
    pageTitle { $('main h4') }

    editButton { $('button', text:'Edit') }

    numberField { $('#aquifer-view-number') }
    nameField { $('#aquifer-view-name') }

    successAlert { $('#aquifer-success-alert') }
  }

  private final String aquiferName
  private final String aquiferNumber

  /**
   * Constructor.
   *
   * Uses the aquifer's name to at-check the page.
   *
   * @param String the expected aquifer name (required)
   * @param String the expected aquifer number (optional) (defaults to the aquifer number in the url)
   */
  AquiferSummaryPage(String aquiferName, String aquiferNumber=null) {
    this.aquiferName = aquiferName
    this.aquiferNumber = aquiferNumber
  }

  def getAquiferNumber() {
    return aquiferNumber ? aquiferNumber : (browser.getCurrentUrl() =~ /aquifers\/(\d+)$/)[0][1]
  }

  void clickEditButton() {
    editButton.click()
  }

  Boolean editAquiferSuccessAlertDisplayed() {
    return waitFor {
      successAlert.displayed == true &&
      successAlert.text().trim() =~ 'Record successfully updated.'
    }
  }
}
