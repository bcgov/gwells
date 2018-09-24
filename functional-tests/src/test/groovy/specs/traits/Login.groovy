package traits

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
    to HomePage // TODO 1/2 find way to not hardcode HomePage, if possible, and allow any page

    headerModule.loginButton.click()

    at LoginPage

    usernameField.value(user.username)
    passwordField.value(user.password)

    logInButton.click()

    at HomePage // TODO 2/2 as above
  }

  void logInAsAdminUser() {
    login(getUserOne())
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
