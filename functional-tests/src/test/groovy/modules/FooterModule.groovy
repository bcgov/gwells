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
   * Clicks footer menu anchor tags based on the displayed text.
   * @param a map of attributes of the footer menu anchor tag. eg: [text:'footer link text'] (required)
   */
  void clickMenuItem(Map<String, Object> itemSelector) {
    footerBar.$(itemSelector, 'a').click()
  }
}
