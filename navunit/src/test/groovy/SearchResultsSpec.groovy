import geb.spock.GebReportingSpec
import pages.app.SearchPage
import spock.lang.Unroll


class SearchResultsSpec extends GebReportingSpec {

// Feature: Search Results
// In order to view search results as a generic user, I want to be able to see the number of matching search results and have these displayed with minimal scrolling

    String countTest = "";
    String[] str;

    @Unroll

    def "Scenario 1: #TestDesc"() {
        given:
        to SearchPage

        when: "#TestDesc, this will results in 0 found"
        $("input", id:"id_well").value("$WellId")
        $("input", id:"id_addr").value("$Address")
        $("input", id:"id_legal").value("$LegalId")
		$("input", id:"id_owner").value("$Owner")
        $("input", id:"submit-id-s").click()

        then: "No records message should be shown"
        if("$ShowError" == "Yes")
			assert waitFor {($("em",id:"em-no-records-found").displayed == true)}
		else
		{
			assert waitFor {($("em",id:"em-no-records-found").displayed == false)}
			assert waitFor {($("div",id:"results_info").displayed == true)}

			def str = $("div",id:"results_info").text().split(' ')
			assert (str[1] == "1") //From entry
			//assert (str[3] == "1") // To entry
            assert (str[5] == "$NumberResult") //Total entries found
		}
   

        where:
        TestDesc 													| WellId          	| Address                  	| LegalId   		| Owner    			| ShowError    | NumberResult
        "No (zero) matching results - No entry"        				| ""				| ""						| ""				| ""				| "Yes"        | 0
        "No (zero) matching results - Well ID 9999999"				| 9999999			| ""						| ""				| ""				| "Yes"        | 0
        "No (zero) matching results - Address - Random Address"		| ""				| "Random Address"			| ""				| ""				| "Yes"        | 0
        "No (zero) matching results - Legal - 9999999"				| ""				| ""						| 9999999			| ""				| "Yes"        | 0
        "No (zero) matching results - Owner - Random Owner"			| ""				| ""						| ""				| "Random Owner"	| "Yes"        | 0
        "No (zero) matching results - All Fields"					| 9999999			| "Random Address"			| 9999999			| "Random Owner"	| "Yes"        | 0
        "One matching result - Well ID - 107667"					| 107667			| ""						| ""				| ""				| "No"         | 1
        "One matching result - Address - 21231 16TH"				| ""				| "218 RD"					| ""				| ""				| "No"         | 1
        "One matching result - Legal PID - 026737680"				| ""				| ""						| "026737680"		| ""				| "No"         | 1
        "One matching result - Owner - GARY AKLES"					| ""				| ""						| ""				| "GARY AKLES"		| "No"         | 1
        "One matching result - - All Fields"						| 107667			| "218 RD"					| "026737680"		| "GARY AKLES"		| "No"         | 1
        "Multiple matching results - Well ID 123"                   | 123               | ""                        | ""                | ""                | "No"         | 2
    } 

    // Searches for Longitude and Latitude - typically through the map.
    def "Scenario 1: Map Search - 0 Results"() {
        given:
        to SearchPage

        when: "The selection will results in 0 found"
        go "/ajax/map_well_search/?start_lat_long=49.112597836986616%2C-122.57641553878786&end_lat_long=49.109788627999635%2C-122.57078289985658"
        go "/search?well=&addr=&legal=&owner=&start_lat_long=49.112597836986616%2C-122.57641553878786&end_lat_long=49.109788627999635%2C-122.57078289985658"

        then: "No records message should be shown"
        assert waitFor {($("em",id:"em-no-records-found").displayed == true)}
    } 
        def "Scenario 1: Map Search - >0 Results"() {
        given:
        to SearchPage

        when: "The selection will results in multiple found"
        go "/ajax/map_well_search/?start_lat_long=48.69073375613481%2C-123.46036434173585&end_lat_long=48.679400715963894%2C-123.43783378601076"
        go "/search?well=&addr=&legal=&owner=&start_lat_long=48.69073375613481%2C-123.46036434173585&end_lat_long=48.679400715963894%2C-123.43783378601076"

        then: "No error msg is shown"
        assert waitFor {($("em",id:"em-no-records-found").displayed == false)}
        assert waitFor {($("div",id:"results_info").displayed == true)}

        def str = $("div",id:"results_info").text().split(' ')
        assert (str[1] == "1") //From entry
        //assert (str[3] == "1") // To entry
        assert (str[5] > "1") //Total entries found
    } 
}