import geb.spock.GebReportingSpec
import pages.app.SearchPage
import pages.app.WellSummaryPage
import spock.lang.Unroll


class WellSearchS1Spec extends GebReportingSpec {

// Feature: Well Search
// In order to find a well as a generic user, I want to be able to search for a well using search criteria

    String[] str;

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
		   	well_id.value("$WellId")
			submit_button.click()

        then: "I should see the wells matching the entered Well Tag Number OR Well Identification Plate Number displayed in the search results"
			if("$ShowError" == "Yes")
				assert waitFor { not_found_msg.displayed == true }
			else
			{
				assert waitFor {($("em",id:"em-no-records-found").displayed == false)}
				assert waitFor { results_info.displayed == true }

				def str = results_info.text().split(' ')
				assert (str[5] == "$NumberResult") //Total entries found

				//println "Results Table: $results_table"

				def n = 0
				def m = 0
				while(n < "$NumberResult".toInteger()) {
            		m=n+1
            		if ("$TagID" == "tag") {
						// assert $("a",text:"$WellId")
						assert waitFor {($('#results > tbody > tr:nth-child('+ m.toString() +') > td:nth-child(1) > a').text() == "$WellId")}
/*						println "n: " + n.toString()
						println results_table[0 + (11 * n)]
            			println results_table[1 + (11 * n)]*/
            			
            			n="$NumberResult".toInteger()
            			}
					else {
/*						println "n: " + n.toString()
						println results_table[0 + (11 * n)]
            			println results_table[1 + (11 * n)] 

*/						def strWellId = $('#results > tbody > tr:nth-child('+ m.toString() +') > td:nth-child(1)').text()
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

				def str = results_info.text().split(' ')
				assert (str[5] == "$NumberResult") //Total entries found

				def n = 0
				def m = 0
				while(n < "$NumberResult".toInteger()) {
            		m=n+1
            		if ("$TagID" == "tag") {
						$('#results > tbody > tr:nth-child('+ m.toString() +') > td:nth-child(1) > a').click()
						
/*						println "n: " + n.toString()
						println results_table[0 + (11 * n)]
            			println results_table[1 + (11 * n)]
*/            			
            			at WellSummaryPage
						assert waitFor {($("span",id:"well_tag_number").text() == "$WellId")}
            			
            			n="$NumberResult".toInteger()
					}
					else {
/*						println "n: " + n.toString()
						println results_table[0 + (11 * n)]
            			println results_table[1 + (11 * n)] 

*/						def strWellId = $('#results > tbody > tr:nth-child('+ m.toString() +') > td:nth-child(1)').text()
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
            		
            				


/*				if ("$TagID" == "tag") {
					$("a",text:"$WellId").click()

					at WellSummaryPage
					assert waitFor {($("span",id:"well_tag_number").text() == "$WellId")}
				}
				else {
					$('#results > tbody > tr:nth-child(2) > td:nth-child(1) > a').click()
					
					at WellSummaryPage
					assert waitFor { identification_plate_number.text() == "$WellId" }
					assert waitFor { well_tag_number.text() == "$SecondID" }
				}	

			}*/

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