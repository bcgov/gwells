package pages

class InformationPage extends BaseAppPage {
  static at = { pageTitle.text() == 'Groundwater Information' }
  static url = '/groundwater-information'
  static content = {
    pageTitle { $('#main-content h2') }
  }
}
