package pages

class SubmissionsConfirmSubmitModal extends BaseAppPage {
  static at = { modalModule.isOpen(modalSelector) }
  static content = {
    modalSelector(wait:true) { $('#confirmSubmitModal') }

    saveButton { $('button', type:'button', text:'Save') }
    cancelButton { $('button', type:'button', text:'Cancel') }
  }

  /**
   * Waits for the modal window to open.
   * Clicks the 'Delete' button.
   * Waits for the modal window to close.
   */
  void confirmSubmit() {
    modalModule.isOpen(modalSelector)
    saveButton.click()
    modalModule.isClosed(modalSelector)
  }
}
