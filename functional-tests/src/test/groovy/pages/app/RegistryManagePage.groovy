
package pages

class RegistryManagePage extends BaseAppPage {
  static at = { pageTitle.text() == 'Groundwater Well Search' }
  static url = '/registries/organizations/manage'
  static content = {
    pageTitle { $('#main-content h2') }

    wellTagOrPlateField { $('#id_well') }
    streetAddressField { $('#id_addr') }
    legalPlanOrDistrictLotOrPIDField { $('#id_legal') }
    ownerNameField { $('#id_owner') }

    searchButton { $('input', type:'submit', value:'Search') }

    searchResultsTable(required:false) { $('#results') }
  }
}
