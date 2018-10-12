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
 * Contains objects and methods for interacting with generic page links.
 */
class CommonLinkModule extends Module {

  /**
   * Attempts to find and click a link on the page.
   *
   * @param a map of attributes of the desired anchor tag. eg: [text:'footer link text']. (required)
   * @param a selector to narrow the search space. (required)
   */
  void clickPageLink(Map<String, Object> itemSelector, Navigator parentSelector) {
    parentSelector.$(itemSelector, 'a').click()
  }
}
