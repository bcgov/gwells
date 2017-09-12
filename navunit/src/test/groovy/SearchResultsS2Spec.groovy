import geb.spock.GebReportingSpec
import pages.app.SearchPage
import spock.lang.Unroll


class SearchResultsS2Spec extends GebReportingSpec {

// Feature: Search Results
// In order to view search results as a generic user, I want to be able to see the number of matching search results and have these displayed with minimal scrolling

    String[] str;

    @Unroll

//Scenario 2: One or more matching results
//Given I have <count> search results
//When I view all search results
//Then I should see <count_message> displayed above the search results
//And the screen should jump (shift focus) to the search results
//      Examples:
//      | count |    count_message    |
//      |  13   | 1-13 of 13 results  |
//      |  127  | 1-25 of 127 results |

    def "Scenario 2: #TestDesc"() {
        given: "I have <count> search results"
        to SearchPage

        $("input", id:"id_well").value("$WellId")
        $("input", id:"id_addr").value("$Address")
        $("input", id:"id_legal").value("$LegalId")
        $("input", id:"id_owner").value("$Owner")
        $("input", id:"submit-id-s").click()

        when: "I view all search results"

        then: "I should see <count_message> displayed above the search results"

        if("$ShowError" == "Yes")
            assert waitFor {($("em",id:"em-no-records-found").displayed == true)}
        else
        {
            assert waitFor {($("em",id:"em-no-records-found").displayed == false)}
            assert waitFor {($("div",id:"results_info").displayed == true)}

            def str = $("div",id:"results_info").text().split(' ')
            assert (str[1] == "1") //From entry
            if ( "$NumberResult".toInteger() < 10){
                assert (str[3] == "$NumberResult") // To entry
            }
            else {
                assert (str[3] == "10") // To entry
            }
            assert (str[5] == "$NumberResult") //Total entries found
        }
        //And the screen should jump (shift focus) to the search results - Not Implemented
        where:
        TestDesc                                                    | WellId            | Address                   | LegalId           | Owner             | ShowError    | NumberResult
        "One matching result - Well ID - 107667"                    | 107667            | ""                        | ""                | ""                | "No"         | 1
        "One matching result - Address - 21231 16TH"                | ""                | "218 RD"                  | ""                | ""                | "No"         | 1
        "One matching result - Legal PID - 026737680"               | ""                | ""                        | "026737680"       | ""                | "No"         | 1
        "One matching result - Owner - GARY AKLES"                  | ""                | ""                        | ""                | "GARY AKLES"      | "No"         | 1
        "One matching result - - All Fields"                        | 107667            | "218 RD"                  | "026737680"       | "GARY AKLES"      | "No"         | 1
        "Multiple matching results - Well ID 123"                   | 123               | ""                        | ""                | ""                | "No"         | 2
        "Multiple matching results - Address 123"                   | ""                | "123"                     | ""                | ""                | "No"         | 139
        "Multiple matching results - Owner ROLAND"                  | ""                | ""                        | ""                | "ROLAND"          | "No"         | 48
    } 
}
