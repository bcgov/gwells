import geb.spock.GebReportingSpec
import spock.lang.*

@Title("Error Page Message")
@Narrative("""Add capacity in the error pages to consume application generated messages if they are present, and display a default error page 
if no message has been generated. This would allow better reporting to end users of the application faults they encounter.""")
@See("https://trello.com/c/R6PqdIEV")
class ErrorPageMessageSpecs extends GebReportingSpec {

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/R6PqdIEV")
    def "Scenario: 1 - Error message"(){
        given "I am regular user"
        and "an application error occurs"
        when "the error page shows"
        then "an application generated error message is displayed."
     }
}