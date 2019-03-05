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
 * Contains objects and methods for interacting with modal pages.
 *
 * Due to the nature of modal windows opening without a url change, and often with some delay for a smoother user
 *  experience, it is important to call isOpen() once before interacting with the modal in any way.
 * Likewise, call isClosed() once after all modal interactions, one of which should close the modal, to ensure the modal
 *  has fully closed.
 */
class ModalModule extends Module {
  static content = {
    modalWindow(required:false) { $('.modal') }
  }

  /**
   * Wait for the modal window to open (be displayed).
   * @param a custom modal selector to use instead of the generic default. Necessary if multiple modal windows are
   *  present on the page. (optional)
   */
  boolean isOpen(Navigator modalSelector = modalWindow) {
    waitFor { modalSelector.displayed }
  }

  /**
   * Wait for any modal windows to close (be not displayed).
   */
  boolean isClosed(Navigator modalSelector = modalWindow) {
    waitFor { modalSelector.displayed == false }
  }
}
