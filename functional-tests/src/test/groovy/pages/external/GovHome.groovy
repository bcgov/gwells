package pages.external

import geb.Page

class GovHome extends Page {
    static at = { title == "B.C. Homepage - Province of British Columbia"}
    static url = "https://www2.gov.bc.ca/"
}