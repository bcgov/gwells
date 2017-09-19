import geb.spock.GebReportingSpec
import pages.app.SearchPage
import pages.app.WellSummaryPage
import spock.lang.Unroll


class WellSearchS5Spec extends GebReportingSpec {

// Feature: Well Search
// In order to find a well as a generic user, I want to be able to search for a well using search criteria

    @Unroll

/* Scenario 5: Well Search using multiple search parameter fields
	Given I am a generic user
		And I want to search for a well by Owner Name AND Street Address
 	When I enter a complete or partial owner name in the Owner Name field
 		And I enter a complete or partial street address in the Street Address field 
 	And click Search 
  	Then I should see wells containing the entered owner name and street address information displayed in the search results
  		And each search result will include a link to the associated well details page
  		And where there are no matching search results the message "No well records could be found." is displayed

** Does this need to be enhanced to describe the use of boolean logic (AND vs. OR)?
 */

    def "Scenario 4: Well Search by Owner Name - #TestDesc"() {
        given: "I am a generic user"
		and: "I want to search for a well by Owner Name AND Street Address"
			to SearchPage
 
        when: "I enter a complete or partial owner name in the Owner Name field"
        	owner_id.value("$Owner")
        
        and: "And I enter a complete or partial street address in the Street Address field"
            address.value("$Address") 	
		
		and: "click search"
			submit_button.click()

        then: "I should see wells containing the entered owner name information displayed in the search result"
	
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }
			else
			{
	         	assert CheckResultTable("$Address") == true
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
        TestDesc                        					| Owner	       	|Address| ShowError    | NumberResult
        "Multiple Results - Gary"							| "GARY"	   	|""		| "No"     	   | 428
        "Single Result - Gary Akles"     					| "GARY AKLES" 	|""		| "No"         | 1	
        "No matching results - Random Owner"    			| "Random Owner"|""		| "Yes"        | 0
        "No matching results - Random Address"    			| ""			|"Random Address"		| "Yes"        | 0
        "No matching results - Random Owner/Address"    	| "Random Owner"|"Random Address"		| "Yes"        | 0
        "No matching results - <null>"         				| ""		    |""		| "Yes"        | 0
        "One matching result - Address - 21231 16TH AVE."	|""				| "21231 16TH AVE."| "No"         | 1
        "Multiple matching results - Address - 123"     	|""| "123"            | "No"         | 139	
        "Multiple matching results - Address - 16TH"     	|""| "16TH"           | "No"         | 389
       	"Partial Owner/Address - Gary/201"					| "GARY"	   		  |"201"		| "No"     	   | 3
        "Full Owner/ partial Address - John Smith/lake"		| "JOHN SMITH"	   	  |"LAKE"		| "No"     	   | 2
        "Partial Owner/Full Address - Gary/201"				| "GARY"	   		  |"TELEGRAPH RD"		| "No"     	   | 1
    } 
}