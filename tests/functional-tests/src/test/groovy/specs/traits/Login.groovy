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

package specs.traits

import pages.HomePage
import pages.LoginPage

/**
 * Methods to manage logging in.
 */
trait Login implements Users {

  /**
   * Log a user in.
   *
   * @param a Map containing username and password keys. eg: [username:'someUsername', password:'somePassword']
   */
  void login(Map user) {
    to HomePage // TODO 1/2 find way to not hardcode HomePage, if possible, and allow any page?

    headerModule.loginButton.click()

    at LoginPage

    usernameField.value(user.username)
    passwordField.value(user.password)

    logInButton.click()

    at HomePage // TODO 2/2 as above
  }

  void logInAsAdminUser() {
    login(getAdminUser())
  }

  void logInAsViewerUser() {
    login(getViewerUser())
  }

  void logInAsSubmissionUser() {
    login(getSubmissionUser())
  }

  void logInAsRegistryUser() {
    login(getRegistryUser())
  }
}
