import geb.spock.GebReportingSpec
import spock.lang.*

@Title("Upload documents to online repository")
@Narrative("""As an administrator, I need to save files to the LAN (source of truth) then upload to the public repository.""")
@See("https://trello.com/c/YEA1EyEs")
class UploadDocumentsSpecs extends GebReportingSpec {

    @Unroll
    @Ignore("Verified Manually")
    @Issue("https://trello.com/c/YEA1EyEs")
    def "Scenario: 1 - Upload Docments"(){
        given: "I am a GWELLS system administrator"
        and: "I routinely have new scanned records to add or edit"
        when: "I upload these files to the public cloud based repository'"
        then: "they will be added/updated and displayed on the Well Summary page"
     }
}