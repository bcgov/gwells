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

/**
 * Contains objects and methods for interacting with the global footer bar.
 */
class FooterModule extends Module {
  static content = {
    footerBar { $('footer') }
  }

  /**
   * Clicks a footer menu anchor tag based on its text.
   * @param footerText the text of the footer link to be clicked. (required)
   */
  void clickMenuItem(String footerText) {
    waitFor {
      footerBar.$('a', text:"$footerText").click()
    }
  }
}
