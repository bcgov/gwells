package pages.app

import geb.Page
import geb.Module

class SurveAdminPage extends Page {
    static at = { title == "Groundwater Wells Site Admin - Province of British Columbia" }
    static url = "gwells/site_admin"

    static content = {
        introtext { $("input", id:"id_survey_introduction_text") }
        link { $("input", id:"id_survey_link" )}
        selectpage { $("select", id:"id_survey_page") }
        enabledcheck { $("checkbox", id:"id_survey_enabled") }
        addupdatebutton { $("button", type:"submit") }
        deletebutton { $("#update-survey > div > div:nth-child(6) > button") }
    }

    //Hard wait function, sometimes useful to sync up the application when you cannot use waitFor.
    void sleepForNSeconds(int n) {
    def originalMilliseconds = System.currentTimeMillis()
    waitFor(n + 1, 0.5) { (System.currentTimeMillis() - originalMilliseconds) > (n * 1000) }
    }    
}