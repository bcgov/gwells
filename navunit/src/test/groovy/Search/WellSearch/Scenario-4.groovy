import geb.spock.GebReportingSpec
import pages.app.SearchPage
import pages.app.WellSummaryPage
import spock.lang.Unroll


class WellSearchS4Spec extends GebReportingSpec {

// Feature: Well Search
// In order to find a well as a generic user, I want to be able to search for a well using search criteria

    @Unroll

/* Scenario 4: Well Search by Owner Name
	Given I am a generic user
		And I want to search for a well by Owner Name
 	When I enter a complete or partial owner name in the Owner Name
 		And click search
  	Then I should see wells containing the entered owner name information displayed in the search results
  		And each search result will include a link to the associated well details page
  		And where there are no matching search results the message "No well records could be found." is displayed
 */

    def "Scenario 4: Well Search by Owner Name - #TestDesc"() {
        given: "I am a generic user"
		and: "And I want to search for a well by Owner Name"
			to SearchPage
 
        when: "I enter a complete or partial owner name in the Owner Name"
        	owner_id.value("$Owner")
		and: "click search"
			submit_button.click()

        then: "I should see wells containing the entered owner name information displayed in the search result"
	
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }
			else
			{
	         	assert CheckResultTable("$Owner") == true
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
        TestDesc                        		| Owner	       	| ShowError    | NumberResult
        "Multiple Results - Gary"				| "GARY"	   	| "No"     	   | 428
        "Single Result - Gary Akles"     		| "GARY AKLES" 	| "No"         | 1	
        "No matching results - Random Owner"    | "Random Owner"| "Yes"        | 0
        "No matching results - <null>"         	| ""		    | "Yes"        | 0
    } 
}