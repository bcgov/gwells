package specs

import pages.HomePage
import pages.RegistryPage

import spock.lang.Timeout
import spock.lang.Title
import spock.lang.Narrative

@Timeout(300)
@Title('Groundwater Well Registry User Tests')
@Narrative('''As developer, I want to verify which features a registry user has access to.''')
class RegistryRoleSpecs extends LoggedInSpec {

  void setup() {
    logInAsRegistryUser()
  }

  void 'Header "Submit Report" link is not present'() {
    given: 'I am logged in as a user with the "Registry" role group'
    when: 'I navigate to the Home page'
    then: 'The "Submit Report" link is not present'
      expectNotPresent(headerModule.getHeaderSelector([text:'Submit Report']))
  }

  void 'Registry page "Add new entry" button is present'() {
    given: 'I am logged in as a user with the "Registry" role group'
    when: 'I navigate to the registry page'
      to RegistryPage
    then: 'The "Add new entry" buttons is present'
      expectPresent(addNewEntryButton)
  }

  void 'Registry page "Manage companies" button is present'() {
    given: 'I am logged in as a user with the "Registry" role group'
    when: 'I navigate to the registry page'
      to RegistryPage
    then: 'The "Manage companies" button is present'
      expectPresent(manageCompaniesButton)
  }

  void 'Registry "Registration status" dropdown filter is present'() {
    given: 'I am logged in as a user with the "Registry" role group'
    when: 'I navigate to the registry page'
      to RegistryPage
    then: 'The "Registration status" dropdown filter is present'
      expectPresent(registrationStatusDropdown)
  }
}
