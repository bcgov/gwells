package pages

class ConfirmRegisterAsWellDrillerModal extends BaseAppPage {
  static at = { modalModule.isOpen(modalSelector) }
  static content = {
    modalSelector(wait:true) { modalModule.modalWindow.has('h5', text:'Confirm register as Well Driller') } //TODO add id if possible

    confirmButton { modalSelector.$('#register-confirm') }
    cancelButton { modalSelector.$('#register-cancel') }
  }

  /**
   * Waits for the modal window to open.
   * Clicks the 'Confirm' button.
   * Waits for the modal window to close.
   */
  void confirmRegisterAsWellDriller() {
    modalModule.isOpen(modalSelector)
    confirmButton.click()
    modalModule.isClosed(modalSelector)
  }
}
