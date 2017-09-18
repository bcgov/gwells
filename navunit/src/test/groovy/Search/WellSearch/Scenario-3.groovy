import geb.spock.GebReportingSpec
import pages.app.SearchPage
import pages.app.WellSummaryPage
import spock.lang.Unroll


class WellSearchS3Spec extends GebReportingSpec {

// Feature: Well Search
// In order to find a well as a generic user, I want to be able to search for a well using search criteria

    @Unroll

/* Scenario 3: Well Search by Legal Plan or District Lot or PID
	Given I am a generic user
		And I want to search for a well by Legal Plan or District Lot or PID
 	When I enter a Legal Plan, District Lot or PID information in the Legal Description field
 		And click search
  	Then I should see wells containing the entered Legal Plan, District Lot or PID information displayed in the search results
  		And each search result will include a link to the associated well details page
  		And where there are no matching search results the message "No well records could be found." is displayed
 */

    def "Scenario 3: Well Search by Plan,Lot or PID - #TestDesc"() {
        given: "I am a generic user"
		and: "I want to search for a well by Legal Plan or District Lot or PID"
			to SearchPage
 
        when: "I enter a Legal Plan, District Lot or PID information in the Legal Description field"
        	legal_id.value("$LegalId")
		and: "click search"
			submit_button.click()

        then: "I should see wells containing the entered Legal Plan, District Lot or PID information displayed in the search results"
        
        //println "Results Table: $results_table"
		
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }
			else
			{
	         	assert CheckResultTable("$LegalId") == true
	         }	

        and: "each search result will include a link to the associated well details page"
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }
			else
			{
				assert waitFor {($("em",id:"em-no-records-found").displayed == false)}
				assert waitFor {($("div",id:"results_info").displayed == true)}

				assert (NumberOfEntriesFound() == "$NumberResult") //Total entries found

				def foundWellID = $('#results > tbody > tr:nth-child(1) > td:nth-child(1) > a').text()
				$('#results > tbody > tr:nth-child(1) > td:nth-child(1) > a').click()
         		
         		at WellSummaryPage
				assert waitFor {($("span",id:"well_tag_number").text() == foundWellID)}
			}
		
		and: "And where there are no matching search results the message -No well records could be found.- is displayed"
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }		

        where:
        TestDesc                        					| LegalId	       | ShowError    | NumberResult
        "Plan - 14313"										| "14313"		   | "No"    	  | 11
        "Lot - 123"     									| "123"            | "No"         | 794	
        "PID - 008710902"     								| "008710902"      | "No"         | 1
        "No matching results - Legal ID - 999999"         	| "999999"         | "Yes"        | 0
        "No matching results - Legal ID - <null>"         	| ""		       | "Yes"        | 0
    } 
}