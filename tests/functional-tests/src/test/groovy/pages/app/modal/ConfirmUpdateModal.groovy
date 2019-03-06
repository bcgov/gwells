package pages

class ConfirmUpdateModal extends BaseAppPage {
  static at = { modalModule.isOpen(modalSelector) }
  static content = {
    modalSelector(wait:true) { $('#orgUpdateModal') }

    saveButton { $('button', type:'button', text:'Save') }
    cancelButton { $('button', type:'button', text:'Cancel') }
  }

  /**
   * Waits for the modal window to open.
   * Clicks the 'Save' button.
   * Waits for the modal window to close.
   */
  void confirmSave() {
    modalModule.isOpen(modalSelector)
    saveButton.click()
    modalModule.isClosed(modalSelector)
  }
}
