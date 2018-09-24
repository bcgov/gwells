package pages

class SubmissionsPage extends BaseAppPage {
  static at = { pageTitle.text() == 'Well Activity Submission' }
  static url = '/submissions'
  static content = {
    pageTitle { $('.card-title .col-lg-8') } // TODO improve this selector
  }
}
