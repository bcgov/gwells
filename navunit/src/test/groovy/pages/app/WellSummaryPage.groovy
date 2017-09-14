package pages.app

import geb.Page

class WellSummaryPage extends Page {
    static at = { title == "Groundwater Wells Well Summary - Province of British Columbia" }
//    static url = "/well"

    static content = {
        well_tag_number { $("span", id:"well_tag_number") } 
        identification_plate_number { $("span", id:"identification_plate_number") } 
    }
}
