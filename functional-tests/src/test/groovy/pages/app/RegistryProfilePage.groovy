
package pages

/**
 * Well Operator profile page.
 */
class RegistryProfilePage extends BaseAppPage {
  static at = { verifyProfilePage() }
  static content = {
    pageTitle { $('main h4') }
  }

  private final String surname
  private final String firstname

  /**
   * Constructor.
   *
   * Uses the well oeprator's first and last name to at check the page, as the title is based on the operator's name.
   *
   * @param String the well operator surname (required)
   * @param String the well operator firstname (required)
   */
  RegistryProfilePage(String surname, String firstname) {
    this.surname = surname
    this.firstname = firstname
  }

  Boolean verifyProfilePage() {
    browser.getCurrentUrl() =~ /\/registries\/people\/[a-z0-9\-]+$/ && pageTitle.text() == "$firstname $surname"
  }
}
