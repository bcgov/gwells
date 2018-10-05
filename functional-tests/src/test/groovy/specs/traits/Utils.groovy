package traits

import geb.navigator.Navigator
import geb.driver.CachingDriverFactory
import geb.waiting.WaitTimeoutException

import java.lang.AssertionError

/**
 * Generic re-usable utility methods.
 */
trait Utils {
  /**
   * Clears the browser and closes it.
   * The next spec to run will open a fresh browser instance.
   */
  void clearAndResetBrowser() {
    resetBrowser()
    CachingDriverFactory.clearCacheAndQuitDriver()
  }

  /**
   * Throw an AssertionError with the given message.
   *
   * @param String exception message. (optional, default: '')
   */
  void fail(String message='') {
    throw new AssertionError(message)
  }

  /**
   * Asserts that the given selector is not present on the page.
   *
   * @param Navigator the geb selector to assert is not present. (required)
   * @param int time in seconds to wait before assuming the selector is not present.
   *   Necessary if the selector typically becomes present after a delay. (optional, default: 1)
   * @return true if the selector is not found.
   * @throws AssertionError if the selector is found.
   */
  Boolean expectNotPresent(Navigator selector, int wait=1) {
    try {
      waitFor(1) { selector }
      fail("Expected the [$selector] selector to not be present, but was found.");
    } catch (WaitTimeoutException e) {
      true
    }
  }

  /**
   * Asserts that the given selector is present on the page.
   *
   * @param Navigator the geb selector to assert is present. (required)
   * @param int time in seconds to wait before agreeing the selector is not present.
   *   Necessary if the selector typically becomes present after a delay. (optional, default: 1)
   * @return true if the selector is found.
   * @throws AssertionError if the selector is not found.
   */
  Boolean expectPresent(Navigator selector, int wait=1) {
    try {
      waitFor(1) { selector }
    } catch (WaitTimeoutException e) {
      fail("Expected the [$selector] selector to be present, but was not found.");
    }
  }
}
