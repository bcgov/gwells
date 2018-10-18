import geb.spock.GebReportingSpec
import pages.app.SearchPage
import geb.Module.*

import spock.lang.Ignore
import spock.lang.Issue
import spock.lang.Narrative
import spock.lang.See
import spock.lang.Specification
import spock.lang.Title
import spock.lang.Unroll    

@Ignore()
@Narrative('''In order to view search results as a generic user, 
        I want to be able to see the number of matching search results and have these displayed with minimal scrolling.''')
@Title('Feature: Search Results')
class SearchResultsSpecs extends GebReportingSpec {

    @Unroll    
    def "Scenario 1: #TestDesc"() {
        given:
        to SearchPage
        
        when: "#TestDesc, this will result in #NumberResult found"
        
        SearchWell("$WellId", "$Address","$LegalId","$Owner")
        at SearchPage

        then: "If 0 results were found: No records message should be shown"
        if("$ShowError" == "Yes") {
			assert waitFor { not_found_msg.displayed == true }
        }
		
        then: "If > 1000 results were found: Too many records message should be shown"
        if("$TooMany" == "Yes") {
            assert waitFor { too_many_found_msg.displayed == true }
        }

        then: "If no error, the actual result will be shown."
        if("$ShowError" == "No" && "$TooMany" == "No") 
        {
			assert waitFor { results_info.displayed == true }

			def str = results_info.text().split(' ')
			assert (str[1] == "1") //From entry
			//assert (str[3] == "1") // To entry
            assert (str[5] == "$NumberResult") //Total entries found
		}
   

        where:
        TestDesc 													| WellId          	| Address                  	| LegalId   		| Owner    			| ShowError    | TooMany | NumberResult
        "No (zero) matching results - No entry"        				| ""				| ""						| ""				| ""				| "Yes"        | "No"    | 0
        "No (zero) matching results - Well ID 9999999"				| "9999999"			| ""						| ""				| ""				| "Yes"        | "No"    | 0
        "No (zero) matching results - Address - Random Address"		| ""				| "Random Address"			| ""				| ""				| "Yes"        | "No"    | 0
        "No (zero) matching results - Legal - 9999999"				| ""				| ""						| "9999999"			| ""				| "Yes"        | "No"    | 0
        "No (zero) matching results - Owner - Random Owner"			| ""				| ""						| ""				| "Random Owner"	| "Yes"        | "No"    | 0
        "No (zero) matching results - All Fields"					| "9999999"			| "Random Address"			| "9999999"			| "Random Owner"	| "Yes"        | "No"    | 0
        "One matching result - Well ID - 107667"					| "107667"			| ""						| ""				| ""				| "No"         | "No"    | 1
        "One matching result - Address - 218 RD"	     			| ""				| "218 RD"					| ""				| ""				| "No"         | "No"    | 1
        "One matching result - Legal PID - 005337879"				| ""				| ""						| "005337879"		| ""				| "No"         | "No"    | 1
        "One matching result - Legal PID - KAP 55997"               | ""                | ""                        | "KAP 55997"       | ""                | "No"         | "No"    | 1
        "One matching result - Legal PID - KAP61460"                | ""                | ""                        | "KAP61460"        | ""                | "No"         | "No"    | 1
        "Multiple matching results - Legal PID - KAP61"             | ""                | ""                        | "KAP61"           | ""                | "No"         | "No"    | 5
        "One matching result - Owner - GARY AKLES"					| ""				| ""						| ""				| "GARY AKLES"		| "No"         | "No"    | 1
        "One matching result - - All Fields"						| "107667"			| "218 RD"					| "BCP21690"		| "GARY AKLES"		| "No"         | "No"    | 1
        "Multiple matching results - Well ID 110000"                | "110000"          | ""                        | ""                | ""                | "No"         | "No"    | 1
        "Too many results - Address 1"                              | ""                | "1"                       | ""                | ""                | "No"         | "Yes"   | 9999
        "Too many results - Legal PID 1"                            | ""                | ""                        | "1"               | ""                | "No"         | "Yes"   | 9999
    } 

    // Searches for Longitude and Latitude - typically through the map.
    def "Scenario 1: Map Search - 0 Results"() {
        given:
        to SearchPage

        when: "The selection will results in 0 found"
        
        // Need to use jquery.val here because webdriver does not allow you put values in a hidden field
        start_lat_long.jquery.val("49.112597836986616,-122.57641553878786")
        end_lat_long.jquery.val("49.109788627999635,-122.57078289985658")
        submit_button.click()

        then: "No records message should be shown"
        assert waitFor { not_found_msg.displayed == true }
    }
    
    def "Scenario 1: Map Search - > 0 Results"() {
        given:
        to SearchPage

        when: "The selection will results in multiple found"

        // Need to use jquery.val here because webdriver does not allow you put values in a hidden field
        start_lat_long.jquery.val("48.69566283264445,-123.47697257995607")
        end_lat_long.jquery.val("48.67299642073175,-123.43191146850587")
        submit_button.click()

        then: "No error msg is shown"
            //If you expect the element not to be there (no error), you cannot use the static definition from the page class
            assert waitFor { results_info.displayed == true }

            def str = results_info.text().split(' ')
            assert (str[1] == "1") //From entry
            assert (str[5] > "1") //Total entries found
    }

    def "Scenario 1: Map Search - > 1000 Results"() {
        given: "I select a large area on the map and search for wells"
        to SearchPage

        when: "The selection will result in more than 1000 wells found"

        // Need to use jquery.val here because webdriver does not allow you put values in a hidden field
        start_lat_long.jquery.val("49.403824657885124,-122.93975830078126")
        end_lat_long.jquery.val("49.04506962208049,-122.21878051757814")
        submit_button.click()

        then: "Too many results error msg is shown"
            assert waitFor { too_many_found_msg.displayed == true }
    }


    @Unroll

    def "Scenario 2: #TestDesc"() {
        given: "I have <count> search results"
        to SearchPage

        SearchWell("$WellId", "$Address","$LegalId","$Owner")

        when: "I view all search results"

        then: "I should see <count_message> displayed under the search results"

        if("$ShowError" == "Yes")
            assert waitFor { not_found_msg.displayed == true }
        else
        {
            assert waitFor {($("div",id:"results_info").displayed == true)}

            assert waitFor { results_info.displayed == true }

            def str = results_info.text().split(' ')
            if ( "$NumberResult".toInteger() < 10){
                assert (str[3] == "$NumberResult") // To entry
            }
            else {
                assert (str[3] == "10") // To entry
            }
            assert (str[5] == "$NumberResult") //Total entries found
        }
        //And the screen should jump (shift focus) to the search results - Not Implemented
        where:
        TestDesc                                                    | WellId            | Address                   | LegalId           | Owner             | ShowError    | NumberResult
        "One matching result - Well ID - 107667"                    | 107667            | ""                        | ""                | ""                | "No"         | 1
        "One matching result - Address - 218 RD"                    | ""                | "218 RD"                  | ""                | ""                | "No"         | 1
        "One matching result - Legal PID - 005337879"               | ""                | ""                        | "005337879"       | ""                | "No"         | 1
        "One matching result - Owner - GARY AKLES"                  | ""                | ""                        | ""                | "GARY AKLES"      | "No"         | 1
        "One matching result - - All Fields"                        | "107667"          | "218 RD"                  | "BCP21690"       | "GARY AKLES"      | "No"         | 1
        "Multiple matching results - Address 12"                    | ""                | "12"                     | ""                | ""                | "No"         | 363
        "Multiple matching results - Owner ROLAND"                  | ""                | ""                        | ""                | "ROLAND"          | "No"         | 12
    }     

//  As a general public user I want to be able to begin a new search with an easy way to remove previous search criteria.
    def "Scenario 3: Reset Button"() {
        given: "that I am a general public user"
            to SearchPage
            SearchWell("107667", "218 RD","026737680","GARY AKLES")
        and: "I want to start a new search"
        when: "I click on the Reset button"
            reset_button.click()
        then: "I should see all previous search criteria removed and the map reset to it's original zoom level"
            assert ( well_id == ""  ) 
            assert ( address == ""  )
            assert ( legal_id == "" )
            assert ( owner_id == "" )
            assert ( map_zoomlevel.text() == "500 km" )            
    }

//  As a general public user I want to be able to zoom in and out of the map so that I can see wells 
//  both up close and far away.
    def "Scenario 4: Zoom in/out buttons on map"() {
        given: "that I am a general public user"
            to SearchPage
        and: "I want to zoom in and out on the map"
        when: "I click on the plus button"
            // starting position
            assert waitFor { ( map_zoomlevel.text() == "500 km" ) }
            zoom_in.click()
        then: "the map should zoom in"
            assert waitFor { ( map_zoomlevel.text() == "200 km" ) }
        when: "I click on the minus button"
            // starting position
            assert waitFor { ( map_zoomlevel.text() == "200 km" ) }
            zoom_out.click()
        then: "the map should zoom out"
            assert waitFor { ( map_zoomlevel.text() == "500 km" ) } 
    }

//  As a general public user, when I have reached the 5km scale, I need a prompt to let me know that I have to search for wells in this area in order to find my well.
    def "Scenario 5: Zoom Tool Function"() {
        given: "that I am doing a map based search on the Search tool"
            to SearchPage
            assert waitFor { ( map_zoomlevel.text() == "500 km" ) }
        and: "I have selected the zoom tool box"
        when: "I zoom to a scale of 5 km"
            while ( map_zoomlevel.text() != "5 km" ){
                zoom_in.click()
                // Slowing down the clicks a bit to allow to system to stay in sync
                sleepForNSeconds(2)
            } 
            assert waitFor { ( map_zoomlevel.text() == "5 km" ) }
        then: "I should see a box appear on the map that states 'Search Wells In This Area'"
            assert waitFor { ( map_search_wells.displayed == true )  }
    }
//  As a general public user, when I forget to enter any search data in the available text boxes, I want an error message to show me my mistakes so that I can try my search again.
    def "Scenario 6: No Search Criteria Error Message"() {
        given: "that I am looking for a welll"
            to SearchPage
        and: "I am searching using any of the available text fields"
        when: "I forget to enter any data"
            SearchWell("", "","","")
        then: "I should see a red warning label appear above the well tag number and well identification plate number field that states 'At least 1 search field is required'"
            assert waitFor { one_search_field_req.displayed == true } 
        and: "a yellow warning label appear under the Groundwater Well Search that states 'No well records could be found'"
            assert waitFor { not_found_msg.displayed == true }    
    }

    @Unroll
    //As a general public user I want to be able to choose how many search results to display on one page.
    def "Scenario 7: Choose Number of search results to be displayed."() {
        given: "As a general public user I want to be able to choose how many search results to display on one page."
        to SearchPage

        when: "#TestDesc, this will result in #NumberResult found"
        
            SearchWell("$WellId", "$Address","$LegalId","$Owner")
            at SearchPage

            assert waitFor { results_info }
            assert waitFor { NumberEntryTo() == "10" }
            
        and: "I select Show 25 entries,"
            def select = $(name: "results_length").module(geb.module.Select)
            select.selected = "25"
           
            assert select.selected == "25"
            assert select.selectedText == "25"

        then: "25 entries will be shown"
            
            assert waitFor { results_info }
            assert waitFor { NumberEntryTo() == "25" }


        where:
        TestDesc                                                    | WellId            | Address                   | LegalId           | Owner             | NumberResult
        "Multiple matching results - Address 12"             | ""                | "12"                     | ""                | ""                | 363
        "Multiple matching results - Owner GARY"              | ""                | ""                        | ""                | "GARY"            | 55
    }

    @Unroll
    //As a general public user, I want to be able to sort the search results table to be better able 
    //to organize and see the results of my search in order to help me find my well.

    def "Scenario 8: Sort numeric column"() {
        given: "I have completed a text search using any criteria."
                to SearchPage
                SearchWell("$WellId", "$Address","$LegalId","$Owner")
            at SearchPage
        and: "And I have received search results in the table located below the map and text fields"     
            assert waitFor { results_info }

        when: "I select the sort arrow beside a numeric column name"
        def original_content = $('#results > tbody > tr:nth-child(1) > td.sorting_1 > a').text().toInteger()
        $('#results > thead > tr > th:nth-child(1)').click()
        sleepForNSeconds(2)
        
        then: "Then the table should re-sort ascending or descending depending on which column was selected."
        def new_content = $('#results > tbody > tr:nth-child(1) > td.sorting_1 > a').text().toInteger()
        assert original_content < new_content

        where:
        TestDesc                                                    | WellId            | Address                   | LegalId           | Owner             | NumberResult
        "Multiple matching results - Address 12"             | ""                | "12"                     | ""                | ""                | 363
        "Multiple matching results - Owner GARY"              | ""                | ""                        | ""                | "GARY"            | 55
    }

       def "Scenario 9: Sort string column"() {
        given: "I have completed a text search using any criteria."
                to SearchPage
                SearchWell("", "$Address","","$Owner")
            at SearchPage
        and: "And I have received search results in the table located below the map and text fields"     
            assert waitFor { results_info }

        when: "I select the sort arrow beside a numeric column name"
        def original_content = $('#results > tbody > tr:nth-child(1) > td:nth-child(1)').text()
        $('#results > thead > tr > th:nth-child(1)').click()
        sleepForNSeconds(2)
        
        then: "Then the table should re-sort ascending or descending depending on which column was selected."
        def new_content = $('#results > tbody > tr:nth-child(1) > td:nth-child(1)').text()

        assert original_content.toInteger() <= new_content.toInteger()

        where:
        TestDesc                                                    | WellId            | Address                   | LegalId           | Owner             | NumberResult
        "Multiple matching results - Address 12"             | ""                | "12"                     | ""                | ""                | 363
        "Multiple matching results - Owner GARY"              | ""                | ""                        | ""                | "GARY"            | 55
    }
}