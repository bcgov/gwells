import geb.spock.GebReportingSpec
import pages.app.SearchPage
import spock.lang.*
import geb.Module

class SearchResultsSpec extends GebReportingSpec {
 
// Feature: Search Results
// In order to view search results as a generic user, I want to be able to see the number of matching search results and have these displayed with minimal scrolling

/*    String countTest = "";
    String[] str;*/

    @Unroll

    def "Scenario 1: #TestDesc"() {
        given:
        to SearchPage

        when: "#TestDesc, this will results in 0 found"
        
        SearchWell("$WellId", "$Address","$LegalId","$Owner")

        then: "No records message should be shown"
        if("$ShowError" == "Yes")
			assert waitFor { not_found_msg.displayed == true }
		else
		{
			assert waitFor { $("em",id:"em-no-records-found").displayed == false }
			assert waitFor { results_info.displayed == true }

			def str = results_info.text().split(' ')
			assert (str[1] == "1") //From entry
			//assert (str[3] == "1") // To entry
            assert (str[5] == "$NumberResult") //Total entries found
		}
   

        where:
        TestDesc 													| WellId          	| Address                  	| LegalId   		| Owner    			| ShowError    | NumberResult
        "No (zero) matching results - No entry"        				| ""				| ""						| ""				| ""				| "Yes"        | 0
        "No (zero) matching results - Well ID 9999999"				| "9999999"			| ""						| ""				| ""				| "Yes"        | 0
        "No (zero) matching results - Address - Random Address"		| ""				| "Random Address"			| ""				| ""				| "Yes"        | 0
        "No (zero) matching results - Legal - 9999999"				| ""				| ""						| "9999999"			| ""				| "Yes"        | 0
        "No (zero) matching results - Owner - Random Owner"			| ""				| ""						| ""				| "Random Owner"	| "Yes"        | 0
        "No (zero) matching results - All Fields"					| "9999999"			| "Random Address"			| "9999999"			| "Random Owner"	| "Yes"        | 0
        "One matching result - Well ID - 107667"					| "107667"			| ""						| ""				| ""				| "No"         | 1
        "One matching result - Address - 21231 16TH"				| ""				| "218 RD"					| ""				| ""				| "No"         | 1
        "One matching result - Legal PID - 026737680"				| ""				| ""						| "026737680"		| ""				| "No"         | 1
        "One matching result - Legal PID - KAP 69982"               | ""                | ""                        | "KAP 69982"       | ""                | "No"         | 1
        "One matching result - Legal PID - KAP67303"                | ""                | ""                        | "KAP67303"        | ""                | "No"         | 1
        "Multiple matching results - Legal PID - KAP67"             | ""                | ""                        | "KAP67"           | ""                | "No"         | 21
        "One matching result - Owner - GARY AKLES"					| ""				| ""						| ""				| "GARY AKLES"		| "No"         | 1
        "One matching result - - All Fields"						| "107667"			| "218 RD"					| "026737680"		| "GARY AKLES"		| "No"         | 1
        "Multiple matching results - Well ID 123"                   | "123"             | ""                        | ""                | ""                | "No"         | 2
    } 

    // Searches for Longitude and Latitude - typically through the map.
    def "Scenario 1: Map Search - 0 Results"() {
        given:
        to SearchPage

        when: "The selection will results in 0 found"
        //go "/ajax/map_well_search/?start_lat_long=49.112597836986616%2C-122.57641553878786&end_lat_long=49.109788627999635%2C-122.57078289985658"
        //go "/search?well=&addr=&legal=&owner=&start_lat_long=49.112597836986616%2C-122.57641553878786&end_lat_long=49.109788627999635%2C-122.57078289985658"
        
        // Need to use jquery.val here because webdriver does not allow you put values in a hidden field
        start_lat_long.jquery.val("49.112597836986616,-122.57641553878786")
        end_lat_long.jquery.val("49.109788627999635,-122.57078289985658")
        submit_button.click()

        then: "No records message should be shown"
        assert waitFor { not_found_msg.displayed == true }
    } 
        def "Scenario 1: Map Search - >0 Results"() {
        given:
        to SearchPage

        when: "The selection will results in multiple found"
        //go "/ajax/map_well_search/?start_lat_long=48.69073375613481%2C-123.46036434173585&end_lat_long=48.679400715963894%2C-123.43783378601076"
        //go "/search?well=&addr=&legal=&owner=&start_lat_long=48.69073375613481%2C-123.46036434173585&end_lat_long=48.679400715963894%2C-123.43783378601076"

        // Need to use jquery.val here because webdriver does not allow you put values in a hidden field
        start_lat_long.jquery.val("48.69073375613481,-123.46036434173585")
        end_lat_long.jquery.val("48.679400715963894,-123.43783378601076")
        submit_button.click()

        then: "No error msg is shown"
            //If you expect the element not to be there (no error), you cannot use the static definition from the page class
            assert waitFor { $("em",id:"em-no-records-found").displayed == false }
            assert waitFor { results_info.displayed == true }

            def str = results_info.text().split(' ')
            assert (str[1] == "1") //From entry
            //assert (str[3] == "1") // To entry
            assert (str[5] > "1") //Total entries found

/*            println "Results Table: $results_table"
            println results_table[0]
            println results_table[11]
            println results_table[12]*/
    }
    @Unroll

    def "Scenario 2: #TestDesc"() {
        given: "I have <count> search results"
        to SearchPage

        SearchWell("$WellId", "$Address","$LegalId","$Owner")

        when: "I view all search results"

        then: "I should see <count_message> displayed above the search results"

        if("$ShowError" == "Yes")
            assert waitFor { not_found_msg.displayed == true }
        else
        {
            assert waitFor {($("em",id:"em-no-records-found").displayed == false)}
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
        "One matching result - Address - 21231 16TH"                | ""                | "218 RD"                  | ""                | ""                | "No"         | 1
        "One matching result - Legal PID - 026737680"               | ""                | ""                        | "026737680"       | ""                | "No"         | 1
        "One matching result - Owner - GARY AKLES"                  | ""                | ""                        | ""                | "GARY AKLES"      | "No"         | 1
        "One matching result - - All Fields"                        | 107667            | "218 RD"                  | "026737680"       | "GARY AKLES"      | "No"         | 1
        "Multiple matching results - Well ID 123"                   | 123               | ""                        | ""                | ""                | "No"         | 2
        "Multiple matching results - Address 123"                   | ""                | "123"                     | ""                | ""                | "No"         | 139
        "Multiple matching results - Owner ROLAND"                  | ""                | ""                        | ""                | "ROLAND"          | "No"         | 48
    }     
}