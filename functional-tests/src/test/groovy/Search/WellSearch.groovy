import geb.spock.GebReportingSpec
import pages.app.SearchPage
import pages.app.WellSummaryPage

import spock.lang.Ignore
import spock.lang.Issue
import spock.lang.Narrative
import spock.lang.See
import spock.lang.Specification
import spock.lang.Title
import spock.lang.Unroll

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

           		println "Tag ID: $TagID"
           		if ("$TagID" == "tag") {
					//println "$WellId"
					//println "Well ID: " + $('#results > tbody > tr:nth-child('+ ReturnRow("$WellId").toString() +') > td.sorting_1 > a').text()
					$('#results > tbody > tr:nth-child('+ ReturnRow("$WellId").toString() +') > td.sorting_1 > a').click()
       				at WellSummaryPage
						assert waitFor { ($("span",id:"well_tag_number").text() == "$WellId") }
					}
				else {
					//println "$SecondID"
					//println "SecondID: " + $('#results > tbody > tr:nth-child('+ ReturnRow("$SecondID").toString() +') > td.sorting_1 > a').text()
					$('#results > tbody > tr:nth-child('+ ReturnRow("$SecondID").toString() +') > td.sorting_1 > a').click()
       				at WellSummaryPage
						assert waitFor { ($("span",id:"well_tag_number").text() == "$SecondID") }
					}
			}
            		
		and: "And where there are no matching search results the message -No well records could be found.- is displayed"
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }		

        where:
        TestDesc                                                    | WellId           | ShowError    | NumberResult	|TagID 	| SecondID
        "One matching result - Well Tag - 107667"                   | 107667           | "No"         | 1				|"tag"	|""
        "One matching result - Well ID 52471"         		        | 52471            | "No"         | 1				|"ID"	|"113308"
        "No matching results - Well ID 999999"                   	| 999999           | "Yes"        | 0				|"tag"	|""
    } 
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
		and: "click search"
			SearchWell("", "$Address","","")

        then: "I should see wells containing the entered street address information displayed in the search results"
        
		
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }
			else
			{
	         	//assert results_table.join(",").indexOf("$Address") >= -1
	         	assert waitFor { results_info.displayed == true }
	         	assert waitFor { CheckResultTable("$Address") == true }
	         }	

		and: "each search result will include a link to the associated well details page"
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }
			else
			{
				assert waitFor { results_info.displayed == true }
				assert (NumberOfEntriesFound() == "$NumberResult") //Total entries found
				def value = $('#results > tbody > tr:nth-child(1) > td.sorting_1 > a').text()
				$('#results > tbody > tr:nth-child(1) > td.sorting_1 > a').click()
       			at WellSummaryPage
					assert waitFor { ( $('#well_tag_number').text() == value ) }
		
			}
  		
		and: "And where there are no matching search results the message -No well records could be found.- is displayed"
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }		

        where:
        TestDesc                        					| Address          | ShowError    | NumberResult
        "One matching result - Address - 4123 WRIGHT STREET "	| "4123 WRIGHT STREET "| "No"         | 1
        "Multiple matching results - Address - 123"     	| "123"            | "No"         | 29	
        "Multiple matching results - Address - 16TH"     	| "16TH"           | "No"         | 18
        "No matching results - Address - 999999"         	| "999999"         | "Yes"        | 0
        "No matching results - Address - <null>"         	| ""		       | "Yes"        | 0
    }

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
		and: "click search"
			SearchWell("", "","$LegalId","")

        then: "I should see wells containing the entered Legal Plan, District Lot or PID information displayed in the search results"
        
		
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }
			else
			{
	         	assert waitFor {($("div",id:"results_info").displayed == true)}
	         	assert waitFor { CheckResultTable("$LegalId") == true }
	         }	

		and: "each search result will include a link to the associated well details page"
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }
			else
			{
				assert waitFor { results_info.displayed == true }
				assert (NumberOfEntriesFound() == "$NumberResult") //Total entries found
				def value = $('#results > tbody > tr:nth-child(1) > td.sorting_1 > a').text()
				$('#results > tbody > tr:nth-child(1) > td.sorting_1 > a').click()
       			at WellSummaryPage
					assert waitFor { ($("span",id:"well_tag_number").text() == value) }
			}
		
		and: "And where there are no matching search results the message -No well records could be found.- is displayed"
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }		

        where:
        TestDesc                        					| LegalId	       | ShowError    | NumberResult
        "Plan - 54433"										| "54433"		   | "No"    	  | 1
        "Lot - 123"     									| "123"            | "No"         | 116
        //"PID - 008710902"     								| "008710902"      | "No"         | 1
        "No matching results - Legal ID - 999999"         	| "999999"         | "Yes"        | 0
        "No matching results - Legal ID - <null>"         	| ""		       | "Yes"        | 0
    } 

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
		and: "click search"
			SearchWell("", "","","$Owner")

        then: "I should see wells containing the entered owner name information displayed in the search result"
	
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }
			else
			{
	         	assert waitFor {($("div",id:"results_info").displayed == true)}
	         	assert waitFor { CheckResultTable("$Owner") == true }
	         }	

		and: "each search result will include a link to the associated well details page"
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }
			else
			{
				assert waitFor { results_info.displayed == true }
				assert (NumberOfEntriesFound() == "$NumberResult") //Total entries found
 				def value = $('#results > tbody > tr:nth-child(1) > td.sorting_1 > a').text()
				$('#results > tbody > tr:nth-child(1) > td.sorting_1 > a').click()
       			at WellSummaryPage
					assert waitFor {($("span",id:"well_tag_number").text() == value) }
			}
		
		and: "And where there are no matching search results the message -No well records could be found.- is displayed"
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }		

        where:
        TestDesc                        		| Owner	       	| ShowError    | NumberResult
        "Multiple Results - Gary"				| "GARY"	   	| "No"     	   | 55
		"Single Result - Gary Akles"     		| "GARY AKLES" 	| "No"         | 1	
        "No matching results - Random Owner"    | "Random Owner"| "Yes"        | 0
        "No matching results - <null>"         	| ""		    | "Yes"        | 0
    } 

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

    def "Scenario 5: Well Search by Owner Name and street address - #TestDesc"() {
        given: "I am a generic user"
		and: "I want to search for a well by Owner Name AND Street Address"
			to SearchPage
 
        when: "I enter a complete or partial owner name in the Owner Name field"
        	//owner_id.value("$Owner")
        
        and: "And I enter a complete or partial street address in the Street Address field"
            //address.value("$Address") 	
		
		and: "click search"
			SearchWell("", "$Address","","$Owner")

        then: "I should see wells containing the entered owner name information displayed in the search result"
	
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }
			else
			{
	         	assert waitFor { results_info.displayed == true }
	         	assert waitFor { CheckResultTable("$Address") == true }
	         	assert waitFor { CheckResultTable("$Owner") == true }
	         }	

		and: "each search result will include a link to the associated well details page"
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }
			else
			{
				assert waitFor { results_info.displayed == true }
				assert (NumberOfEntriesFound() == "$NumberResult") //Total entries found
				def value = $('#results > tbody > tr:nth-child(1) > td.sorting_1 > a').text()
				$('#results > tbody > tr:nth-child(1) > td.sorting_1 > a').click()
       			at WellSummaryPage
					assert waitFor {($("span",id:"well_tag_number").text() == value) }
			}
		
		and: "And where there are no matching search results the message -No well records could be found.- is displayed"
			if("$ShowError" == "Yes")
			    assert waitFor { not_found_msg.displayed == true }

        where:
        TestDesc                                            | Owner         | Address           | ShowError     | NumberResult
        "Multiple Results - Gary"                           | "GARY"        | ""		        | "No"          | 55
        "Single Result - Gary Akles"                        | "GARY AKLES"  | ""		        | "No"          | 1	
        "No matching results - Random Owner"                | "Random Owner"| ""		        | "Yes"         | 0
        "No matching results - Random Address"              | ""            | "Random Address"  | "Yes"         | 0
        "No matching results - Random Owner/Address"        | "Random Owner"| "Random Address"  | "Yes"         | 0
        "No matching results - <null>"                      | ""            | ""		        | "Yes"         | 0
        "One matching result - Address - 1229 LAKE ROAD "	| ""            | "1229 LAKE ROAD " | "No"          | 1
        "Multiple matching results - Address - 123"         | ""            | "123"             | "No"          | 29	
        "Multiple matching results - Address - 16TH"        | ""            | "16TH"            | "No"          | 18
       	"Partial Owner/Address - Gary/7239"                 | "GARY"        | "7239"		    | "No"          | 1
        "Full Owner/ partial Address - Ronald/MALAHAT"      | "RONALD"      | "MALAHAT"		    | "No"          | 1
        "Partial Owner/Full Address - Gary/PILGRIM "        | "GARY"        | "PILGRIM "		| "No"          | 1
    }         
}