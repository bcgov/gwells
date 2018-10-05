package specs

import traits.Login

/**
 * Base spec for tests that require being logged in.
 *
 * All specs that login should extend this class.
 */
abstract class LoggedInSpec extends BaseSpec implements Login {
  /**
   * Cleanup that runs after each test.
   *
   * Clears and restarts the browser, the next test will open in a new browser.
   */
  void cleanup() {
    clearAndResetBrowser()
  }
}
