package specs

import pages.RegistryPage
import pages.OrganizationsPage
import pages.OrganizationsAddModal
import pages.ConfirmUpdateModal
import pages.ConfirmDeleteModal

import spock.lang.Timeout
import spock.lang.Title
import spock.lang.Narrative
import spock.lang.Stepwise

@Timeout(300)
@Stepwise
@Title('Groundwater Well Organizations Tests')
@Narrative('''As an admin user, I want to add, update, and delete organizations (companies).''')
class OrganizationsSpecs extends LoggedInSpec {

  void setup() {
    logInAsAdminUser()

    // TODO replace below 3 lines with "to OrganizationsPage" when fixed:
    // https://trello.com/c/V4iDExNM/1307-epicregistry-cannot-bookmark-urls-in-registry-5
    to RegistryPage
    clickManageCompaniesButton()
    at OrganizationsPage
  }

  void 'Adding a new company'() {
    given: 'I am logged in as an admin user'
    and: 'I click the "Add new company" button'
      clickAddNewCompanyButton()
      at OrganizationsAddModal
    and: 'I populate all required fields for a new company'
      setCompanyName('bdd company')
      setStreetAddress('bdd address')
      setCity('bdd city')
      setProvince('BC')
      setPostalCode('1A1 A1A')
      setTelephoneNumber('1234567890')
      setFaxNumber('123454321')
      setEmail('email@bdd.bdd')
      setWebsite('http://bdd-website.bdd')
    when: 'I save the company'
      clickSaveButton()
    then: 'The company is created'
      at OrganizationsPage
      addCompanySuccessAlertDisplayed()
  }

  void 'Updating a company'() {
    given: 'I am logged in as an admin user'
    and: 'I select a company'
      selectCompany('.*bdd company.*')
    and: 'I make edits to the company'
      setCompanyName('edit company')
      setStreetAddress('edit address')
      setCity('edit city')
      setProvince('AB')
      setPostalCode('2B2 B2B')
      setTelephoneNumber('0987654321')
      setFaxNumber('543212345')
      setEmail('email@edit.edit')
      setWebsite('http://edit-website.edit')
    when: 'I save the edits to the company'
      clickUpdateButton()
      at ConfirmUpdateModal
      confirmSave()
    then: 'The company is updated'
      at OrganizationsPage
      updateCompanySuccessAlertDisplayed()
  }

  void 'Deleting a company'() {
    given: 'I am logged in as an admin user'
    and: 'I select a company'
      selectCompany('.*edit company.*')
    when: 'I delete the company'
      clickDeleteButton()
      at ConfirmDeleteModal
      confirmDelete()
    then: 'The company is deleted'
      at OrganizationsPage
      deleteCompanySuccessAlertDisplayed('edit company')
  }
}
