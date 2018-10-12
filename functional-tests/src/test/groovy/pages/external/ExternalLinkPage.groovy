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

import org.openqa.selenium.NoSuchWindowException

import geb.Page

/**
 * Generic page that represents an external page.
 * This external page may overwrite the current window, or be opened in a new window or tab.
 * Use a new instance of this class as the parameter to an 'at' call.
 *
 * Note: This currently only works when running the tests in headful mode (not headless)!
 *
 * Example:
 *   at new ExternalLinkPage('Fuel Info', 'gov\\.bc\\.ca\\/fuelfacts')
 */
class ExternalLinkPage extends Page {
  static at = {
    Boolean result

    // covers a rare issue where the main thread can sometimes hang indefinitely when dealing with multiple windows.
    // with a separate thread, if it hangs, the test will fail but the remaining test execution can continue.
    Thread thread = Thread.start {
      result = foundTargetWindow()
    }
    thread.join()

    result == true
  }

  private final String windowTitleRegex
  private final String urlRegex
  private final String simpleName

  /**
   * Constructor.
   *
   * @param String windowTitleRegex a regex string that is uniquely contained within the target window title. (required)
   * @param String urlRegex a regex string that will be asserted is contained in the target window url. (required)
   * @param String simpleName a string to use in the spock reports for tests utilizing this class. (Optional, default: 'ExternalLinkPage')
   *
   * Example:
   *   The urlRegex 'someMinistry\\.gov\\.bc' would match 'www.someMinistry.gov.bc.ca/otherParameters'
   */
  ExternalLinkPage(String windowTitleRegex, String urlRegex, String simpleName='ExternalLinkPage') {
    this.windowTitleRegex = windowTitleRegex.trim()
    this.urlRegex = urlRegex.trim()
    this.simpleName = simpleName
  }

  /**
   * Attempts to find the expected window based on the window title and window url.
   * If a window does not have a title, attempt to find the expected window based on url alone.
   *
   * If a new window was opened for this external page, close it.
   * Otherwise do not close the window, as at least 1 window must remain open for test execution to continue.
   */
  Boolean foundTargetWindow() {
    Boolean foundMatchingWindow = false
    try {
      browser.withWindow({ title.trim() =~ windowTitleRegex }, close:shouldCloseWindow()) {
        if (browser.getCurrentUrl() =~ urlRegex) {
          foundMatchingWindow = true
        }
      }
    } catch (NoSuchWindowException e) {
      /**
       * Unable to find a window based on title.
       * Either the expected title is incorrect, or the window is rendering a pdf, which depending on the browser type
       *  may not have a window title.
       * Loop through all open windows and try to find the expected window based on url only.
       *
       * Note: Chrome currently does not expose a window title when rendering PDFs.
       */
      browser.getAvailableWindows().each { windowHandle ->
        browser.withWindow(windowHandle) {
          if (browser.getCurrentUrl() =~ urlRegex) {
            if (shouldCloseWindow()) {
              browser.close()
            }
            foundMatchingWindow = true
          }
        }
      }
    }
    return foundMatchingWindow
  }

  /**
   * Returns true if multiple windows (or tabs) are open, false otherwise.
   */
  Boolean shouldCloseWindow() {
    browser.getAvailableWindows().size() > 1
  }

  /**
   * Prevent calling getSimpleName() from throwing an exception during a spock test:
   *  - Calling getSimpleName() on a class returns just the class name, without any package prefixes.
   *  - Calling getSimpleName() on an instance of a class throws an exception.
   */
  String getSimpleName() {
    simpleName
  }
}
