package specs

import pages.HomePage

import spock.lang.Timeout
import spock.lang.Title
import spock.lang.Narrative

@Timeout(300)
@Title('Groundwater Well Search Tests')
@Narrative('''As a public user, I want to search for existing wells.''')
class SearchSpecs extends BaseSpec {

  void setup() {
    to HomePage
  }

  void 'Search by "Well Tag Number or Well Identification Plate Number" field'() {
    given: 'I populate the "Well Tag Number or Well Identification Plate Number" field'
      setWellTagOrIdentificationPlateNumber(123)
    when: 'I click the Search button'
      clickSearchButton()
    then: 'The search is executed and a list of results is displayed'
      foundSearchResults()
  }

  void 'Search by "Street Address" field'() {
    given: 'I populate the "Street Address" field'
      setStreetAddress('a')
    when: 'I click the Search button'
      clickSearchButton()
    then: 'The search is executed and a table containing at least 1 matching result is displayed'
      foundSearchResults()
  }

  void 'Search by "Legal Plan or District Lot or Parcel Identification Number PID" field'() {
    given: 'I populate the "Legal Plan or District Lot or Parcel Identification Number PID" field'
      setLegalPlanOrDistrictLotorPID('123')
    when: 'I click the Search button'
      clickSearchButton()
    then: 'The search is executed and a table containing at least 1 matching result is displayed'
      foundSearchResults()
  }

  void 'Search by "Owner Name" field'() {
    given: 'I populate the "Owner Name" field'
      setOwnerName('a')
    when: 'I click the Search button'
      clickSearchButton()
    then: 'The search is executed and a table containing at least 1 matching result is displayed'
      foundSearchResults()
  }
}
