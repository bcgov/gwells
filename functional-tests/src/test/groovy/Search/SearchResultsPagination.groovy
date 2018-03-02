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
        		$("#results_paginate a[data-dt-idx=\"$TargetPage\"]").click()	
        	}
        	assert waitFor {(NumberEntryFrom().toInteger() == ("$TargetPage".toInteger() - 1) * 10 + 1 )}


        	//$("#results_paginate a[data-dt-idx=\"$TargetPage\"]").click()
        where:
		    TestDesc 													                          | WellId          | Address                  	| LegalId   		    | Owner    			    | Page    |TargetPage | NumberResult
        "Multiple matching results - Address 12 - 1 to Max"        | ""             	| "12"                     | ""                | ""                | 1    	  |3    	    | 363    
        "Multiple matching results - Address 12 - 1 to 2"          | ""             	| "12"                     | ""                | ""                | 1    	  |2    	    | 363   
        "Multiple matching results - Address 12 - 2 to 3"          | ""             	| "12"                     | ""                | ""                | 2    	  |3    	    | 363   
        "Multiple matching results - Address 12 - 1 to 3"          | ""             	| "12"                     | ""                | ""                | 1    	  |3    	    | 363   
        "Multiple matching results - Address 12 - 3 to 1"          | ""             	| "12"                     | ""                | ""                | 3    	  |1    	    | 363   
        "Multiple matching results - Address 12 - 3 to 2"          | ""             	| "12"                     | ""                | ""                | 3    	  |2    	    | 363   
    } 
        @Unroll
        def "Scenario 2: Next Page links: #TestDesc#Testresult"() {
        given: "I have #NumberResult wells search result"
         to SearchPage

         SearchWell("", "$Address","","")      

         assert waitFor { results_info.displayed == true }
  
        when: "I view all search results from page #Page"
          assert (NumberOfEntriesFound() == "$NumberResult") //Total entries found
          assert waitFor {(CheckPageButton("$Page") == true)}
          $("#results_paginate a[data-dt-idx=\"$Page\"]").click()

        then: "I should see \'Next\' is #Testresult"
          assert waitFor {(next_button.displayed == true)}
          
          if ( "$Testresult" == "enabled" )
          {
            assert waitFor {(next_button.classes().sort() == ["next", "paginate_button"])}
          }
          else
          {
            assert waitFor {(next_button.classes().sort() == ["disabled", "next", "paginate_button"])}
          }
        where:
        TestDesc                                                      | WellId | Address | LegalId | Owner | Page | NumberResult | Testresult
        "Multiple matching results - Address 123 - Next is "  | ""     | "123"   | ""      | ""    | 3    | 29    | "disabled"
        "Multiple matching results - Address 123 - Next is " | ""     | "123"   | ""      | ""    | 1    | 29    | "enabled"
    } 

    @Unroll
    def "Scenario 3: Previous Page links: #TestDesc#Testresult"() {
        given: "I have NumberResult wells search result"
         to SearchPage

         SearchWell("", "$Address","","")
      
         assert waitFor { results_info.displayed == true }
  
        when: "I view all search results from page #Page"
          assert (NumberOfEntriesFound() == "$NumberResult") //Total entries found
          assert waitFor {(CheckPageButton("$Page") == true)}
          $("#results_paginate a[data-dt-idx=\"$Page\"]").click()

        then: "I should see \'Previous\' is #Testresult."
          assert waitFor {(previous_button.displayed == true)}  
        if ( "$Testresult" == "enabled" )
          {
            assert waitFor {(previous_button.classes().sort() == ["paginate_button", "previous"])}
          }
          else
          {
            assert waitFor {(previous_button.classes().sort() == ["disabled", "paginate_button", "previous"])}
          }
        where:
        TestDesc                                                          | WellId | Address | LegalId | Owner | Page | NumberResult | Testresult
        "Multiple matching results - Address 123 - Previous is "  | ""     | "123"   | ""      | ""    | 1    | 29           | "disabled"
        "Multiple matching results - Address 123 - Previous is " | ""     | "123"   | ""      | ""    | 3   | 29            | "enabled"
    } 
}