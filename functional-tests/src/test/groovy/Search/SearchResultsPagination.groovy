import geb.spock.GebReportingSpec
import pages.app.SearchPage
import pages.app.WellSummaryPage

import spock.lang.Unroll
import spock.lang.Ignore
import spock.lang.Issue
import spock.lang.Narrative
//import spock.lang.PendingFeature
import spock.lang.See
import spock.lang.Specification
import spock.lang.Title

@Title("Search Results Pagination")
@Narrative("""
In order to view search results as a generic user, I want search results to be paginated when there more than 25 results
""")
class SearchResultsPaginationSpecs extends GebReportingSpec {

    @Unroll

/* 	Scenario 1: Page links
Given I have <count> search results
 When I view all search results from page <page>
  Then I should see a link to page <target_page>

    Examples:
      |  count | page | target_page |
      |   26   |   1  |       1     |
      |   26   |   1  |       2     |
      |   26   |   2  |       1     |
      |   26   |   2  |       2     |
      |   51   |   1  |       1     |
      |   51   |   1  |       2     |
      |   51   |   1  |       3     |
      |   51   |   2  |       1     |
      |   51   |   2  |       2     |
      |   51   |   2  |       3     |
      |   51   |   3  |       1     |
      |   51   |   3  |       2     |
      |   51   |   2  |       3     |
 */

    def "Scenario 1: Page links: #TestDesc"() {
        given: "I have #NumberResult wells search result"
          to SearchPage

          SearchWell("", "$Address","","")
          
          assert waitFor { results_info.displayed == true }
      
        when: "I view all search results from page #Page"
          assert (NumberOfEntriesFound() == "$NumberResult") //Total entries found
          assert waitFor {(CheckPageButton("$Page") == true)}

          $("#results_paginate a[data-dt-idx=\"$Page\"]").click()
          assert waitFor {(NumberEntryFrom().toInteger() == ("$Page".toInteger() - 1) * 10 + 1 )}

        then: "I should see a link to page #TargetPage"
        	assert waitFor {(CheckPageButton("$TargetPage") == true)}

        	def CalcMax = "$NumberResult".toInteger() / "$TargetPage".toInteger()

        	if ( CalcMax <= 10 ) {
        		$("#results_paginate a[data-dt-idx=\"7\"]").click()	
        	}
        	else {
        		// Last Page shown is always index 7
        		$("#results_paginate a[data-dt-idx=\"$TargetPage\"]").click()	
        	}
        	assert waitFor {(NumberEntryFrom().toInteger() == ("$TargetPage".toInteger() - 1) * 10 + 1 )}


        	//$("#results_paginate a[data-dt-idx=\"$TargetPage\"]").click()
        	

        where:
		    TestDesc 													                          | WellId          | Address                  	| LegalId   		    | Owner    			    | Page    |TargetPage | NumberResult
        "Multiple matching results - Address 12 - 1 to Max"        | ""             	| "12"                     | ""                | ""                | 1    	  |3    	    | 361    
        "Multiple matching results - Address 12 - 1 to 2"          | ""             	| "12"                     | ""                | ""                | 1    	  |2    	    | 361   
        "Multiple matching results - Address 12 - 2 to 3"          | ""             	| "12"                     | ""                | ""                | 2    	  |3    	    | 361   
        "Multiple matching results - Address 12 - 1 to 3"          | ""             	| "12"                     | ""                | ""                | 1    	  |3    	    | 361   
        "Multiple matching results - Address 12 - 3 to 1"          | ""             	| "12"                     | ""                | ""                | 3    	  |1    	    | 361   
        "Multiple matching results - Address 12 - 3 to 2"          | ""             	| "12"                     | ""                | ""                | 3    	  |2    	    | 361   
    } 
        @Unroll
        def "Scenario 2: Next Page links: #TestDesc"() {
        given: "I have #NumberResult wells search result"
         to SearchPage

         SearchWell("", "$Address","","")      

         assert waitFor { results_info.displayed == true }
  
        when: "I view all search results from page <page>"
          assert (NumberOfEntriesFound() == "$NumberResult") //Total entries found
          assert waitFor {(CheckPageButton("$Page") == true)}

          def CalcMax = "$NumberResult".toInteger() / "$Page".toInteger()

          if ( CalcMax <= 10 ) {
            $("#results_paginate a[data-dt-idx=\"7\"]").click()
          }
          else {
            // Last Page shown is always index 7
            $("#results_paginate a[data-dt-idx=\"$Page\"]").click()
          }

        then: "I should see a link \'Next\'"
          assert waitFor {(next_button.displayed == true)}
          
          // Test to see if we are at the end of the list....
          if ( NumberOfEntriesFound() == NumberEntryTo() ) {
            // Next should be disabled
            assert waitFor {(next_button.classes().sort() == ["disabled", "next", "paginate_button"])}
          }
          else {
            // Next is visible and enabled
            assert waitFor {(next_button.classes().sort() == ["next", "paginate_button"])}
          }

       when: "I click \'Next\'"
          $("#results_paginate a[data-dt-idx=\"7\"]").click()

        then: "I should be on page #Page"
          assert waitFor {(next_button.displayed == true)}
          
          // Test to see if we are at the end of the list....
          if ( NumberOfEntriesFound() == NumberEntryTo() ) {
            // Next should be disabled
            assert waitFor {(next_button.classes().sort() == ["disabled", "next", "paginate_button"])}
          }
          else {
            // Next is visible and enabled
            assert waitFor {(next_button.classes().sort() == ["next", "paginate_button"])}
            assert waitFor {(NumberEntryFrom().toInteger() == ("$Page".toInteger()) * 10 + 1 )}
          }

        where:
        TestDesc                                                      | WellId | Address | LegalId | Owner | Page | NumberResult
        "Multiple matching results - Address 12 - Next is disabled"  | ""     | "12"   | ""      | ""    | 3    | 361    
        "Multiple matching results - Address 12 - Next button shows" | ""     | "12"   | ""      | ""    | 1    | 361    
    } 

    @Unroll
    def "Scenario 3: Previous Page links: #TestDesc"() {
        given: "I have NumberResult wells search result"
         to SearchPage

         SearchWell("", "$Address","","")
      
         assert waitFor { results_info.displayed == true }
  
        when: "I view all search results from page <page>"
          assert (NumberOfEntriesFound() == "$NumberResult") //Total entries found
          assert waitFor {(CheckPageButton("$Page") == true)}

        then: "I should see a link \'Previous\'"
          assert waitFor {(previous_button.displayed == true)}

          def CalcMax = "$NumberResult".toInteger() / "$Page".toInteger()

          if ( CalcMax <= 10 ) {
            $("#results_paginate a[data-dt-idx=\"7\"]").click()
          }
          else {
            // Last Page shown is always index 7
            $("#results_paginate a[data-dt-idx=\"$Page\"]").click()
          }
          
          if ( "$Page" == "1") {
            // Previous be disabled
            println "Page should be 1: $Page"
            println previous_button.classes().sort()
            assert waitFor {(previous_button.classes().sort() == ["disabled", "paginate_button", "previous"])}
            assert waitFor {(NumberEntryFrom().toInteger() == ("$Page".toInteger() - 1) * 10 + 1 )}
          }
          else {
            // Previous is visible and enabled
            println "Page should not be 1: $Page"
            println previous_button.classes().sort()
            assert waitFor {(previous_button.classes().sort() == ["paginate_button", "previous"])}
          }

       when: "I click \'Previous\'"
           $("#results_paginate a[data-dt-idx=\"0\"]").click() //Always index 0
           def tmpPage = "$Page".toInteger()
           tmpPage = tmpPage - 1

        then: "I should be on page #Page"
          assert waitFor {(previous_button.displayed == true)}
          
          if ( tmpPage <= 1) {
            // Previous should not be disabled
            assert waitFor {(previous_button.classes().sort() == ["disabled", "paginate_button", "previous"])}
          }
          else {
            // Previous is visible and enabled
            assert waitFor {(previous_button.classes().sort() == ["paginate_button", "previous"])}
            assert waitFor {(NumberEntryFrom().toInteger() == ("$Page".toInteger() - 2) * 10 + 1 )}
          }

        where:
        TestDesc                                                          | WellId | Address | LegalId | Owner | Page | NumberResult
        "Multiple matching results - Address 123 - previous is disabled"  | ""     | "12"   | ""      | ""    | 1    | 361    
        "Multiple matching results - Address 123 - Previous button shows" | ""     | "12"   | ""      | ""    | 3   | 361    
    } 
}