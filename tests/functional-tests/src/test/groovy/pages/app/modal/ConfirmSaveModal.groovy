package pages

class ConfirmSaveModal extends BaseAppPage {
  static at = { modalModule.isOpen(modalSelector) }
  static content = {
    modalSelector(wait:true) { $('#confirmSave') }

    okButton { $('button', type:'button', text:'OK') }
    cancelButton { $('button', type:'button', text:'Cancel') }
  }

  /**
   * Waits for the modal window to open.
   * Clicks the 'OK' button.
   *
   * @param checkClosed enable or disable checking if the modal closed.  This is often necessary if the modal closes
   *  slowly, and the test needs to wait for it to fully close before continuing.  If the modal triggers a change of
   *  page, this check should NOT be enabled as the modal reference is now stale, and cannot be accessed.
   *  (Optional, default: false)
   */
  void confirmSave(Boolean checkClosed=false) {
    modalModule.isOpen(modalSelector)
    okButton.click()
    if (checkClosed) {
      modalModule.isClosed()
    }
  }
}
