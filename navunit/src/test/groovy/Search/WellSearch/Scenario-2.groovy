import geb.spock.GebReportingSpec
import pages.app.SearchPage
import pages.app.WellSummaryPage
import spock.lang.Unroll


class WellSearchS2Spec extends GebReportingSpec {

// Feature: Well Search
// In order to find a well as a generic user, I want to be able to search for a well using search criteria

    @Unroll

/* 	Scenario 2: Well Search by Street Address
	Given I am a generic user
	And I want to search for a well by Street Address
 	When I enter a complete or partial street address in the Address field 
 	And click search
  	Then I should see wells containing the entered street address information displayed in the search results
  	And each search result will include a link to the associated well details page
  	And where there are no matching search results the message "No well records could be found." is displayed
 */

    def "Scenario 2: Well Search by Street Address: #TestDesc"() {
        given: "I am a generic user"
		and: "I want to search for a well by Street Address"
			to SearchPage
 
        when: "I enter a complete or partial street address in the Address field"
		   	address.value("$Address")
		and: "click search"
			submit_button.click()

        then: "I should see wells containing the entered street address information displayed in the search results"
        
        //println "Results Table: $results_table"
		
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }
			else
			{
	         	//assert results_table.join(",").indexOf("$Address") >= -1
	         	assert CheckResultTable("$Address") == true
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
        TestDesc                        					| Address          | ShowError    | NumberResult
        "One matching result - Address - 21231 16TH AVE."	| "21231 16TH AVE."| "No"         | 1
        "Multiple matching results - Address - 123"     	| "123"            | "No"         | 139	
        "Multiple matching results - Address - 16TH"     	| "16TH"           | "No"         | 389
        "No matching results - Address - 999999"         	| "999999"         | "Yes"        | 0
        "No matching results - Address - <null>"         	| ""		       | "Yes"        | 0
    } 
}