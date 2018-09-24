package pages

class RegistryPage extends BaseAppPage {
  static at = { pageTitle.text() == 'Register of Well Drillers and Well Pump Installers' }
  static url = 'registries'
  static content = {
    pageTitle { $('main h4') }

    addNewEntryButton(required:false) { $('#addNewEntryButton') }
    manageCompaniesButton(required:false) { $('#manageCompaniesButton') }

    registrationStatusDropdown(required:false) { $('#manageCompaniesButton') }
  }

  void clickAddNewEntryButton() {
    waitFor { addNewEntryButton.click() }
  }

  void clickManageCompaniesButton() {
    waitFor { manageCompaniesButton.click() }
  }
}
