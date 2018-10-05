package pages

class HomePage extends BaseAppPage {
  static at = { pageTitle.text() == 'Groundwater Well Search' }
  static url = ''
  static content = {
    pageTitle { $('#main-content h2') }

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
