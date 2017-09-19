import geb.spock.GebReportingSpec
import pages.app.SearchPage
import pages.app.WellSummaryPage
import spock.lang.Unroll

class SearchResultsPaginationS2Spec extends GebReportingSpec {

// Feature: Search Results Pagination
// In order to view search results as a generic user, I want search results to be paginated when there more than 25 results

    @Unroll

/* 	Scenario 2: Next Page links
Given I have <count> search results
 When I view all search results from page <page>
  Then I should see a link "Next >>"

   When I click "Next >>"
    Then I should be on page <next_page> 
      Examples:
        | count | page | next_page |
        |  26   |   1  |      2    |
        |  26   |   2  |     N/A   |
        |  51   |   1  |      2    |
        |  51   |   2  |      3    |
        |  51   |   3  |     N/A   |
 */

    def "Scenario 2: Next Page links: #TestDesc"() {
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

        then: "I should be on page <next_page>"
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
		    TestDesc 													                            | WellId | Address | LegalId | Owner | Page | NumberResult
        "Multiple matching results - Well ID 123 - Next is disabled"  | ""     | "123"   | ""      | ""    | 14   | 139    
        "Multiple matching results - Well ID 123 - Next button shows" | ""     | "123"   | ""      | ""    | 1    | 139    
    } 
}