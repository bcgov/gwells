package pages.app

import geb.Page
import geb.Module

class SearchPage extends Page {
    static at = { title == "Groundwater Wells Search - Province of British Columbia" }
    static url = "/search"

    static content = {
        well_id { $("input", id:"id_well") } 
        address { $("input", id:"id_addr") }
        legal_id { $("input", id:"id_legal") }
		owner_id { $("input", id:"id_owner") }
        start_lat_long { $("input", name:"start_lat_long", type:"hidden") }
        end_lat_long { $("input", name:"end_lat_long", type:"hidden") }
        submit_button { $("input", id:"submit-id-s") }
        not_found_msg { $("em",id:"em-no-records-found") }
        results_info { $("div",id:"results_info") }
        results_table { $("#results td")*.text() }
    }
}
