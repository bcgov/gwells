package pages

import geb.Page

class LoginPage extends Page {
  static at = {
    title.trim() == 'Log in to Groundwater Wells' &&
    pageTitle.text().trim() == 'GROUNDWATER WELLS'
  }
  static content = {
    pageTitle { $('#kc-header-wrapper') }

    usernameField { $('#username') }
    passwordField { $('#password') }

    logInButton { $('input', type:'submit', value:'Log in') }
  }
}
