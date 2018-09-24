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

class RegistryAddPage extends BaseAppPage {
  static at = { pageTitle.text() == 'Add new applicant' }
  static url = 'registries/people/add'
  static content = {
    pageTitle { $('main h5') }

    surnameField { $('#surnameInput') }
    firstnameField { $('#firstnameInput') }
    telephoneNumberField { $('#contactTelInput') }
    emailField { $('#contactEmailInput') }
    wellDrillerORCSFIeld { $('#drillerORCSInput') }
    pumpInstallerORCSField { $('#pumpORCSInput') }

    registerAsRadioButtons { $('#registrationTypeInput') }

    saveButton { $('button', type:'submit', text:'Save') }
  }

  void setSurname(String surname) {
    surnameField.value(surname)
  }

  void setFirstname(String firstname) {
    firstnameField.value(firstname)
  }

  void setTelephoneNumber(String telephoneNumber) {
    telephoneNumberField.value(telephoneNumber)
  }

  void setEmail(String email) {
    emailField.value(email)
  }

  void setWellDrillerROCS(int orcsNumber) {
    wellDrillerORCSFIeld.value(orcsNumber)
  }

  void setPumpInstallerORCS(int orcsNumber) {
    pumpInstallerORCSField.value(orcsNumber)
  }

  // TODO
  void registerAsDriller() {
    registerAsRadioButtons.$('input', value:'DRILL').click()
  }

  // TODO
  void registerAsPumpInstaller() {
    registerAsRadioButtons.$('input', value:'PUMP').click()
  }

  void clickSaveButton() {
    saveButton.click()
  }
}
