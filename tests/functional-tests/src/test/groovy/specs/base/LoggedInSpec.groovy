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

package specs

import specs.traits.Login

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
