import geb.spock.GebReportingSpec
import pages.app.SearchPage
import pages.app.WellSummaryPage
import spock.lang.Unroll

class SearchResultsPaginationS3Spec extends GebReportingSpec {

// Feature: Search Results Pagination
// In order to view search results as a generic user, I want search results to be paginated when there more than 25 results

    @Unroll

/* 	Scenario 3: Previous Page links
Given I have <count> search results
 When I view all search results from page <page>
  Then I should see a link "<< Previous "

   When I click "<< Previous"
    Then I should be on page <previous_page> 
      Examples:
        | count | page | previous_page |
        |  26   |   1  |      N/A      |
        |  26   |   2  |       1       |
        |  51   |   1  |      N/A      |
        |  51   |   2  |       1       |
        |  51   |   3  |       2       |
 */

    def "Scenario 3: Previous Page links: #TestDesc"() {
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

        then: "I should be on page <next_page>"
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
        "Multiple matching results - Well ID 123 - previous is disabled"  | ""     | "123"   | ""      | ""    | 1    | 139    
        "Multiple matching results - Well ID 123 - Previous button shows" | ""     | "123"   | ""      | ""    | 14   | 139    
    } 
}