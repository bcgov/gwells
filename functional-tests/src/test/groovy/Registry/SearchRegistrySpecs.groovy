import geb.spock.GebReportingSpec
import pages.app.RegisterPage
import spock.lang.*

class SearchRegistrySpecs extends GebReportingSpec {

    @Unroll
    def "Search Registry: #TestDesc"(){
       	given: "that I am an general user"
           to RegisterPage
        when: "I search for a registered driller/installer"
            at RegisterPage
            reset
            switch ("$SearchType") {
              case "installer":
                selectinstaller
                break
              case "driller":
                selectdriller
                break
              case "name":
                selectdriller
                search.value("$Search")
                break
              case "community":
                selectdriller
                selectcommunity = ["$Search"]
                break
            }
            submit
        then: "I should find the result"
            if ( "$NumberResult" == "none" ) {
                assert waitFor { noresults.displayed }
            } else {
                assert waitFor { result == "$NumberResult" }
            }

        where:
        TestDesc 					| Search          	| SearchType      | Results             | NumberResult
        "Name=John"                 | "John"			| "name"          | ""				    | "18"
        "Name=Alan"                 | "Alan"			| "name"          | ""				    | "2"
        "Community=Langley"         | "Langley"			| "community"     | ""				    | "8"
        "Community=Aldergrove"      | "Aldergrove"		| "community"     | ""				    | "10"
    }
}
/* Mon  7 May 14:03:44 2018 GW at top of list

        "Empty search criteria"     | ""                | ""              | ""                  | "285"
        "Empty search criteria - Driller"     | ""              | "driller"       | ""          | "285"
        "Empty search criteria - Installer"     | ""            | "installer"     | ""          | "320"

*/
