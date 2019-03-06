package pages

class ConfirmDeleteModal extends BaseAppPage {
  static at = { modalModule.isOpen(modalSelector) }
  static content = {
    modalSelector(wait:true) { $('#orgDeleteModal') }

    saveButton { $('button', type:'button', text:'Delete') }
    cancelButton { $('button', type:'button', text:'Cancel') }
  }

  /**
   * Waits for the modal window to open.
   * Clicks the 'Delete' button.
   * Waits for the modal window to close.
   */
  void confirmDelete() {
    modalModule.isOpen(modalSelector)
    saveButton.click()
    modalModule.isClosed(modalSelector)
  }
}
