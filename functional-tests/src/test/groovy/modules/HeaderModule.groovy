package modules

import geb.Module
import geb.navigator.Navigator

/**
 * Contains objects and methods for interacting with the global header bar.
 */
class HeaderModule extends Module {
  static content = {
    bcLogo { $('.navbar-brand') }

    loginButton { $('#keycloak-auth #gwells-sso-login') }

    headerNavigationBar { $('header #navContainer .navbar-nav') }
  }

  /**
   * Clicks a header menu anchor tag based on its attributes, typically text.
   * @param a map of attributes of the header menu anchor tag. eg: [text:'header link text'] (required)
   */
  void clickMenuItem(Map<String, Object> itemSelector) {
    getHeaderSelector(itemSelector).click()
  }

  /**
   * Returns the selector for a header menu anchor tag based on its attributes, typically text.
   * @param a map of attributes of the header menu anchor tag. eg: [text:'header link text'] (required)
   */
  Navigator getHeaderSelector(Map<String, Object> itemSelector) {
    headerNavigationBar.$(itemSelector, 'a')
  }
}
