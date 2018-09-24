package pages

class OrganizationsPage extends BaseAppPage {
  static at = { pageTitle.text() == 'Manage Companies' }
  static url = ''
  static content = {
    pageTitle { $('main h4') }

    addAlert(required:false) { $('#orgAddSuccessAlert') }
    updateAlert(required:false) { $('#orgUpdateSuccessAlert') }
    deleteAlert(required:false) { $('#orgDeleteSuccessAlert') }

    // add company
    addNewCompanyButton { $('#orgAddNewButton') }

    // Update/Delete company
    selectCompanySearchField { $('#orgEditSelectDropdown').$('input', type:'search') }
    selectCompanyDropdown(required:false) { $('#orgEditSelectDropdown').$('.dropdown-menu') }

    // Update company
    companyNameField(required:false) { $('#orgEditNameInput') }
    streetAddressField(required:false) { $('#orgEditAddressInput') }
    cityField(required:false) { $('#orgEditCityInput') }
    provinceDropdown(required:false) { $('#orgEditProvinceInput') }
    postalCodeField(required:false) { $('#orgEditPostalInput') }
    telephoneNumberField(required:false) { $('#orgEditPhoneInput') }
    faxNumberField(required:false) { $('#orgEditFaxInput') }
    emailField(required:false) { $('#orgEditEmailInput') }
    websiteField(required:false) { $('#orgEditWebsiteInput') }

    updateButton(required:false) { $('button', type:'submit', text:'Update') }

    // Delete company
    deleteButton(required:false) { $('button', type:'button', text:'Delete this company') }
  }

  // Add company
  void clickAddNewCompanyButton() {
    addNewCompanyButton.click()
  }

  Boolean addCompanySuccessAlertDisplayed() {
    return waitFor {
      addAlert.displayed == true &&
      addAlert.text() =~ 'Company added'
    }
  }

  // Update/Delete company
  void selectCompany(String regex) {
    selectCompanySearchField.click()

    interact {
      waitFor {
        moveToElement(selectCompanyDropdown.$('li', text:~"$regex")).click()
      }
    }
  }

  // Update company
  void setCompanyName(String name) {
    companyNameField.value(name)
  }

  void setStreetAddress(String address) {
    streetAddressField.value(address)
  }

  void setCity(String city) {
    cityField.value(city)
  }

  void setProvince(String province) {
    provinceDropdown.$('option', text:province).click()
  }

  void setPostalCode(String postalCode) {
    postalCodeField.value(postalCode)
  }

  void setTelephoneNumber(String telephoneNumber) {
    telephoneNumberField.value(telephoneNumber)
  }

  void setFaxNumber(String faxNumber) {
    faxNumberField.value(faxNumber)
  }

  void setEmail(String email) {
    emailField.value(email)
  }

  void setWebsite(String website) {
    websiteField.value(website)
  }

  void clickUpdateButton() {
    updateButton.click()
  }

  Boolean updateCompanySuccessAlertDisplayed() {
    return waitFor {
      updateAlert.displayed == true &&
      updateAlert.text() =~ 'Successfully updated company information'
    }
  }

  // Delete company
  void clickDeleteButton() {
    waitFor { deleteButton.click() }
  }

  Boolean deleteCompanySuccessAlertDisplayed(String name) {
    return waitFor {
      deleteAlert.displayed == true &&
      deleteAlert.text() =~ "$name removed"
    }
  }
}
