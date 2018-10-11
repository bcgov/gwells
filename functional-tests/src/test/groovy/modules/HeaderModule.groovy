/*
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/

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
    waitFor {
      getHeaderSelector(itemSelector).click()
    }
  }

  /**
   * Returns the selector for a header menu anchor tag based on its attributes, typically text.
   * @param a map of attributes of the header menu anchor tag. eg: [text:'header link text'] (required)
   */
  Navigator getHeaderSelector(Map<String, Object> itemSelector) {
      headerNavigationBar.$(itemSelector, 'a')
  }
}
