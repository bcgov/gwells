package pages.app

import geb.Page

class SearchPage extends Page {
    static at = { title == "Groundwater Wells Search - Province of British Columbia" }
    static url = "/search"

    static content = {
        well_id(wait: true) { $("input", id:"id_well") } 
        address(wait: true) { $("input", id:"id_addr") }
        legal_id(wait: true) { $("input", id:"id_legal") }
		owner_id(wait: true) { $("input", id:"id_owner") }
        start_lat_long(wait: true) { $("input", name:"start_lat_long", type:"hidden") }
        end_lat_long(wait: true) { $("input", name:"end_lat_long", type:"hidden") }
        submit_button(wait: true) { $("input", id:"submit-id-s") }
        not_found_msg { $("div",id:"no-records-found") }
        too_many_found_msg { $("div",id:"too-many-wells") }
        results_info { $("div",id:"results_info") }
        results_table { $("#results td")*.text() }
        page_buttons { $("#results_paginate a")*.text() }
        next_button { $("li",id:"results_next")}
        previous_button { $("li",id:"results_previous")}
    }
    boolean CheckResultTable(String addres_to_check) {
        if(results_table.join(",").indexOf(addres_to_check) >= -1)
            return true
        else
            return false    
    }

    boolean CheckPageButton(String page_button_to_check) {
        if(page_buttons.join(",").indexOf(page_button_to_check) >= -1)
            return true
        else
            return false    
    }
    
    String NumberOfEntriesFound() {
        def str = results_info.text().split(' ')
        return str[5]
    }
    String NumberEntryFrom() {
        def str = results_info.text().split(' ')
        return str[1]
    }
    String NumberEntryTo() {
        def str = results_info.text().split(' ')
        return str[3]
    }

    void SearchWell(String s_well_id, String s_address, String s_legal_id, String s_owner) {        
        waitFor { well_id.value(s_well_id) }
        waitFor { address.value(s_address) }
        waitFor { legal_id.value(s_legal_id) }
        waitFor { owner_id.value(s_owner) }
        submit_button.click()
    }

    void InjectLibrary( String library ){
       def ok = browser.driver.executeScript("document.body.appendChild(document.createElement(\'script\')).src=\'$library\'")
    }
    //InjectLibrary('https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js')
}
