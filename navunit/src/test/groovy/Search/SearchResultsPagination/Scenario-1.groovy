import geb.spock.GebReportingSpec
import pages.app.SearchPage
import pages.app.WellSummaryPage
import spock.lang.Unroll

class SearchResultsPaginationS1Spec extends GebReportingSpec {

// Feature: Search Results Pagination
// In order to view search results as a generic user, I want search results to be paginated when there more than 25 results

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
        given: "I have <count> search result"
			to SearchPage

			well_id.value("$WellId")
        	address.value("$Address")
        	legal_id.value("$LegalId")
			owner_id.value("$Owner")        
			
			submit_button.click()	
			
			assert waitFor { results_info.displayed == true }
	
        when: "I view all search results from page <page>"
			assert (NumberOfEntriesFound() == "$NumberResult") //Total entries found
			assert waitFor {(CheckPageButton("$Page") == true)}

			$("#results_paginate a[data-dt-idx=\"$Page\"]").click()
			assert waitFor {(NumberEntryFrom().toInteger() == ("$Page".toInteger() - 1) * 10 + 1 )}

        then: "I should see a link to page <target_page>"
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
		TestDesc 													| WellId          	| Address                  	| LegalId   		| Owner    			| Page    |TargetPage| NumberResult
        "Multiple matching results - Well ID 123 - 1 to Max"        | ""             	| "123"                     | ""                | ""                | 1    	  |14    	 | 139    
        "Multiple matching results - Well ID 123 - 1 to 2"          | ""             	| "123"                     | ""                | ""                | 1    	  |2    	 | 139    
        "Multiple matching results - Well ID 123 - 2 to 3"          | ""             	| "123"                     | ""                | ""                | 2    	  |3    	 | 139    
        "Multiple matching results - Well ID 123 - 1 to 3"          | ""             	| "123"                     | ""                | ""                | 1    	  |3    	 | 139    
        "Multiple matching results - Well ID 123 - 3 to 1"          | ""             	| "123"                     | ""                | ""                | 3    	  |1    	 | 139    
        "Multiple matching results - Well ID 123 - 3 to 2"          | ""             	| "123"                     | ""                | ""                | 3    	  |2    	 | 139    
    } 
}