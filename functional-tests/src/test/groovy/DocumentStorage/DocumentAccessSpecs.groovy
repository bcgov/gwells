import geb.spock.GebReportingSpec
import spock.lang.*

@Title("Document Access - Public")
@Narrative("""As an application administrator, I need to be able to set user access levels to the documents that are stored and displayed through the GWELLS Application.""")
@See("https://trello.com/c/mptCm5jj")
class DocumentAccessSpecs extends GebReportingSpec {

    @Ignore("Verified Manually")
    @Issue("https://trello.com/c/mptCm5jj")
    def "Scenario: 1 - Document is Accessible"(){
        given: "that I have a well record or other document"
        and: "I want to make the document publicly available to all users"
        when: "I add the document to the public 'bucket'"
        then: "all records in this bucket should be made available to all users."
     }
}