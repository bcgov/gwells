package specs

import pages.RegistryPage
import pages.RegistryAddPage
import pages.RegistryProfilePage

import spock.lang.Timeout
import spock.lang.Title
import spock.lang.Narrative

@Timeout(300)
@Title('Groundwater Well Registry Add Tests')
@Narrative('''As an admin user, I want to register a new well operator.''')
class RegistryAddSpecs extends LoggedInSpec {

  void 'Register a new well operator'() {
    given: 'I am logged in as a admin user'
      logInAsAdminUser()
      // TODO replace below 3 lines with "to RegistryAddPage" when fixed:
      // https://trello.com/c/V4iDExNM/1307-epicregistry-cannot-bookmark-urls-in-registry-5
      to RegistryPage
      clickAddNewEntryButton()
      at RegistryAddPage
    and: 'I populate all required fields to add a new well operator'
      setSurname('surname')
      setFirstname('firstname')
      setTelephoneNumber('123-456-7890')
      setEmail('email@email.email')
      setWellDrillerROCS(1234321)
      setPumpInstallerORCS(5678765)
    when: 'I click the Save button'
      clickSaveButton()
    then: 'The well operator is created and I am taken to the operator profile page'
      at new RegistryProfilePage('surname', 'firstname')
  }
}
