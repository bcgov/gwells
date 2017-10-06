import geb.spock.GebReportingSpec
import pages.app.SearchPage
//import pages.app.WellSummaryPage

import spock.lang.Ignore
import spock.lang.Issue
import spock.lang.Narrative
import spock.lang.See
import spock.lang.Specification
import spock.lang.Title
import spock.lang.Unroll

//#results > tbody > tr:nth-child(1) > td.sorting_1 > a
//#results > tbody > tr:nth-child(2) > td.sorting_1 > a
//#results > thead > tr > th.sorting_desc


@Title("Well Search")
@Narrative("""
In order to find a well as a generic user, I want to be able to search for a well using search criteria
""")
class WellSearchSpecs extends GebReportingSpec {
    @Unroll

/* 	Scenario 1: Well Search by Well Tag Number OR Well Identification Plate Number
	Given I am a generic user
		And I want to search for a well by Well Tag Number OR Well Identification Plate Number
	When I enter a valid Well Tag Number or Well Idenification Plate Number in the Well field 
		And click search
	Then I should see the wells matching the entered Well Tag Number OR Well Identification Plate Number displayed in the search results
		And each search result will include a link to the associated well details page
		And where there are no matching search results the message "No well records could be found." is displayed
 */

    def "Scenario 1: Well Search by Well Tag Number OR Well Identification Plate Number: #TestDesc"() {
        given: "I am a generic user"
        
		and: "I want to search for a well by Well Tag Number OR Well Identification Plate Number"
			to SearchPage
 
        when: "I enter a valid Well Tag Number or Well Idenification Plate Number in the Well field And click search"
			SearchWell("$WellId", "","","")

        then: "I should see the wells matching the entered Well Tag Number OR Well Identification Plate Number displayed in the search results"
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }
			else
			{
				assert waitFor { results_info.displayed == true }
				assert (NumberOfEntriesFound() == "$NumberResult") //Total entries found

           		if ("$TagID" == "tag") {
           			assert waitFor {  ( CheckResultTable("$WellId") == true ) }
           			}
				else {
					assert waitFor {  ( CheckResultTable("$SecondID") == true ) }
					}	
			}
		
		and: "each search result will include a link to the associated well details page"
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }
			else
			{
				assert waitFor { results_info.displayed == true }
				assert (NumberOfEntriesFound() == "$NumberResult") //Total entries found

           		if ("$TagID" == "tag") {
					println "Well ID: " + $('#results > tbody > tr:nth-child('+ ReturnRow("$WellId").toString() +') > td.sorting_1 > a').text()
					$('#results > tbody > tr:nth-child('+ ReturnRow("$WellId").toString() +') > td.sorting_1 > a').click()
					}
				else {
					println "SecondID: " + $('#results > tbody > tr:nth-child('+ ReturnRow("$SecondID").toString() +') > td.sorting_1 > a').text()
					$('#results > tbody > tr:nth-child('+ ReturnRow("$SecondID").toString() +') > td.sorting_1 > a').click()
					}
			}
            		
		and: "And where there are no matching search results the message -No well records could be found.- is displayed"
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }		

        where:
        TestDesc                                                    | WellId           | ShowError    | NumberResult	|TagID 	| SecondID
        "One matching result - Well Tag - 107667"                   | 107667           | "No"         | 1				|"tag"	|""
        "Multiple matching results - Well Tag 123"                  | 123              | "No"         | 2				|"tag"	|""
        "Multiple matching results - Well ID 52471"                 | 52471            | "No"         | 2				|"ID"	|113308
        "No matching results - Well ID 999999"                   	| 999999           | "Yes"        | 0				|"tag"	|""
    }    
}