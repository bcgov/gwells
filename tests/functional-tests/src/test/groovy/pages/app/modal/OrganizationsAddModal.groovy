package pages

class OrganizationsAddModal extends BaseAppPage {
  static at = { modalModule.isOpen(modalSelector) }
  static content = {
    modalSelector(wait:true) { $('#orgAddModal') }

    companyNameField { $('#orgAddNameInput') }
    streetAddressField { $('#orgAddAddressInput') }
    cityField { $('#orgAddCityInput') }
    provinceDropdown { $('#orgAddProvinceInput') }
    postalCodeField { $('#orgAddPostalInput') }
    telephoneNumberField { $('#orgAddPhoneInput') }
    faxNumberField { $('#orgAddFaxInput') }
    emailField { $('#orgAddEmailInput') }
    websiteField { $('#orgAddWebsiteInput') }

    saveButton { $('button', type:'submit', text:'Save') }
  }

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

  void clickSaveButton() {
    saveButton.click()
  }
}
