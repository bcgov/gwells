package pages.external

import geb.Page

class SSO extends Page {
    static at = { title == "Government of British Columbia"}
    static url = "https://logontest.gov.bc.ca/clp-cgi/int/logon.cgi"
}
