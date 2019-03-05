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

package pages

/**
 * Well Operator profile page.
 */
class RegistryProfilePage extends BaseAppPage {
  static at = {
    browser.getCurrentUrl() =~ /\/registries\/people\/[a-z0-9\-]+$/ &&
    pageTitle.text() == "$firstName $surname"
  }
  static content = {
    pageTitle { $('main h4') }
  }

  private final String surname
  private final String firstName

  /**
   * Constructor.
   *
   * Uses the well operator's first and last name to-at check the page, as the title is based on the operator's name.
   *
   * @param String the well operator surname (required)
   * @param String the well operator firstName (required)
   */
  RegistryProfilePage(String surname, String firstName) {
    this.surname = surname
    this.firstName = firstName
  }
}
