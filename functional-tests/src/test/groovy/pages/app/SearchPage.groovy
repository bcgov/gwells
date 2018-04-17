package pages.app

import geb.Page
import geb.Module

class SearchPage extends Page {
    static at = { title == "Groundwater Wells Search - Province of British Columbia" }
    static url = "gwells/search"

    static content = {
        well_id(wait: true) { $("input", id:"id_well") } 
        address(wait: true) { $("input", id:"id_addr") }
        legal_id(wait: true) { $("input", id:"id_legal") }
		owner_id(wait: true) { $("input", id:"id_owner") }
        start_lat_long(wait: true) { $("input", name:"start_lat_long", type:"hidden") }
        end_lat_long(wait: true) { $("input", name:"end_lat_long", type:"hidden") }
        submit_button(wait: true) { $("input", id:"submit-id-s") }
        reset_button(wait: true) { $("a", id:"reset-id-s") }
        not_found_msg { $("div",id:"no-records-found") }
        too_many_found_msg { $("div",id:"too-many-wells") }
        one_search_field_req { $('#id-searchForm > div.alert.alert-block.alert-danger > ul > li') }
        results_info { $("div",id:"results_info") }
        results_table { $("#results td")*.text() }
        page_buttons { $("#results_paginate a")*.text() }
        next_button { $("li",id:"results_next")}
        previous_button { $("li",id:"results_previous")}
        next_button_click { $("li",id:"results_next").$("a")}
        previous_button_click { $("li",id:"results_previous").$("a")}
        map_zoomlevel { $("div", class: "leaflet-control-scale-line") }
        zoom_in { $("a", class: "leaflet-control-zoom-in") }
        zoom_out { $("a", class: "leaflet-control-zoom-out") }
        map_search_wells { $("div", class: "leaflet-control leaflet-area-search") }
    }
    boolean CheckResultTable(String addres_to_check) {
        if(results_table.join(",").indexOf(addres_to_check) >= -1)
            return true
        else
            return false    
    }
    int FindResultIndex(String string_to_check) {
        def nIndex = results_table.join(",").indexOf(string_to_check)

        return nIndex  
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
        if ( s_well_id != "") { waitFor { well_id.value(s_well_id) } }
        if ( s_address != "") { waitFor { address.value(s_address) } }
        if ( s_legal_id != "") { waitFor { legal_id.value(s_legal_id) } }
        if ( s_owner != "") { waitFor { owner_id.value(s_owner) } }
        submit_button.click()
    }

    //Use as InjectLibrary('https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js') to inject dependencies
    void InjectLibrary( String library ){
       def ok = browser.driver.executeScript("document.body.appendChild(document.createElement(\'script\')).src=\'$library\'")
    }

    //Returns the row in the result table based on the wellid or tagnumber supplied.
    int ReturnRow( String s_id ) {
        def n_index = 0
        while ( $('#results > tbody > tr:nth-child('+ n_index.toString() +') > td.sorting_1 > a').text() != s_id  || n_index > 9) {
            n_index++
        }
        return (n_index)
    }

    //Hard wait function, sometimes useful to sync up the application when you cannot use waitFor.
    void sleepForNSeconds(int n) {
    def originalMilliseconds = System.currentTimeMillis()
    waitFor(n + 1, 0.5) { (System.currentTimeMillis() - originalMilliseconds) > (n * 1000) }
    }    
}