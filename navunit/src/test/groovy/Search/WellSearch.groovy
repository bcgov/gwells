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
class WellSearchSpec extends GebReportingSpec {
    @Unroll

/* 	Scenario 1: Well Search by Well Tag Number OR Well Identificaiton Plate Number
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
				assert waitFor {($("em",id:"em-no-records-found").displayed == false)}
				assert waitFor { results_info.displayed == true }

				assert (NumberOfEntriesFound() == "$NumberResult") //Total entries found

				//println "Results Table: $results_table"

				def n = 0
				def m = 0
				while(n < "$NumberResult".toInteger()) {
            		m=n+1
            		if ("$TagID" == "tag") {
						// assert $("a",text:"$WellId")
						assert waitFor {($('#results > tbody > tr:nth-child('+ m.toString() +') > td:nth-child(1) > a').text() == "$WellId")}
						println "n: " + n.toString()
						println results_table[0 + (11 * n)]
            			println results_table[1 + (11 * n)]
            			
            			n="$NumberResult".toInteger()
            			}
					else {
						println "n: " + n.toString()
						println results_table[0 + (11 * n)]
            			println results_table[1 + (11 * n)] 

						def strWellId = $('#results > tbody > tr:nth-child('+ m.toString() +') > td:nth-child(1)').text()
						if( strWellId == "$SecondID") {
            				assert waitFor {($('#results > tbody > tr:nth-child('+ m.toString() +') > td:nth-child(2)').text() == "$WellId")}
							assert waitFor {($('#results > tbody > tr:nth-child('+ m.toString() +') > td:nth-child(1) > a').text() == "$SecondID")}
/*							println "yes, did it!"
*/						}	
					}
            		n++
				}
			}
		
		and: "each search result will include a link to the associated well details page"
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }
			else
			{
				assert waitFor {($("em",id:"em-no-records-found").displayed == false)}
				assert waitFor {($("div",id:"results_info").displayed == true)}

				assert (NumberOfEntriesFound() == "$NumberResult") //Total entries found

				def n = 0
				def m = 0
				while(n < "$NumberResult".toInteger()) {
            		m=n+1
            		if ("$TagID" == "tag") {
						$('#results > tbody > tr:nth-child('+ m.toString() +') > td:nth-child(1) > a').click()
						
						println "n: " + n.toString()
						println results_table[0 + (11 * n)]
            			println results_table[1 + (11 * n)]
           			
            			at WellSummaryPage
						assert waitFor { well_tag_number.text() == "$WellId" }
            			
            			n="$NumberResult".toInteger()
					}
					else {
						println "n: " + n.toString()
						println results_table[0 + (11 * n)]
            			println results_table[1 + (11 * n)] 

						def strWellId = $('#results > tbody > tr:nth-child('+ m.toString() +') > td:nth-child(1)').text()
						if( strWellId == "$SecondID") {
							$('#results > tbody > tr:nth-child('+ m.toString() +') > td:nth-child(1) > a').click()
					
							at WellSummaryPage
							assert waitFor { identification_plate_number.text() == "$WellId" }
							assert waitFor { well_tag_number.text() == "$SecondID" }
						}
					}
					n++
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
        
        println "Results Table: $results_table"
		
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }
			else
			{
	         	//assert results_table.join(",").indexOf("$Address") >= -1
	         	assert waitFor {($("div",id:"results_info").displayed == true)}
	         	assert waitFor { CheckResultTable("$Address") == true }
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
        
        //println "Results Table: $results_table"
		
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
	         	assert waitFor {($("div",id:"results_info").displayed == true)}
	         	assert waitFor { CheckResultTable("$Address") == true }
	         	assert waitFor { CheckResultTable("$Owner") == true }
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