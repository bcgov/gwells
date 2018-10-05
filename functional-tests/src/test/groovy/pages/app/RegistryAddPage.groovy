
package pages

class RegistryAddPage extends BaseAppPage {
  static at = { pageTitle.text() == 'Add new applicant' }
  static url = '/registries/people/add'
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
