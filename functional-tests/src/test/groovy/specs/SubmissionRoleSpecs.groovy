package specs

import pages.HomePage
import pages.RegistryPage

import spock.lang.Timeout
import spock.lang.Title
import spock.lang.Narrative

@Timeout(300)
@Title('Groundwater Well Submission User Tests')
@Narrative('''As developer, I want to verify which features a submission user has access to.''')
class SubmissionRoleSpecs extends LoggedInSpec {

  void setup() {
    logInAsSubmissionUser()
  }

  void 'Header "Submit Report" link is present'() {
    given: 'I am logged in as a user with the "Submission" role group'
    when: 'I navigate to the Home page'
      to HomePage
    then: 'The "Submit Report" link is present'
      expectPresent(headerModule.getHeaderSelector([text:'Submit Report']))
  }

  void 'Registry page "Add new entry" button is not present'() {
    given: 'I am logged in as a user with the "Submission" role group'
    when: 'I navigate to the registry page'
      to RegistryPage
    then: 'The "Add new entry" buttons is not present'
      expectNotPresent(addNewEntryButton)
  }

  void 'Registry page "Manage companies" button is not present'() {
    given: 'I am logged in as a user with the "Submission" role group'
    when: 'I navigate to the registry page'
      to RegistryPage
    then: 'The "Manage companies" button is not present'
      expectNotPresent(manageCompaniesButton)
  }

  void 'Registry "Registration status" dropdown filter is not present'() {
    given: 'I am logged in as a user with the "Submission" role group'
    when: 'I navigate to the registry page'
      to RegistryPage
    then: 'The "Registration status" dropdown filter is not present'
      expectNotPresent(registrationStatusDropdown)
  }
}
