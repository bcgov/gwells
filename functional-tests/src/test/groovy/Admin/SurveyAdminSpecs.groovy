import geb.spock.GebReportingSpec
import spock.lang.*

@Title("Screen to allow adding surveys on the GWELLS application")
@Narrative("""As an application administrator, I need a screen that allows me to easily add surveys on the GWELLS application in order for me to update or add context without having to go through a developer.
""")
@See("https://trello.com/c/SZrt0RLt")
class SurveyAdminSpecs extends GebReportingSpec {

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/SZrt0RLt")
    def "Scenario: 1 - Add Survey"(){
        given: "I am an application administrator"
        and: "I need to add a survey to the GWELLS application screens"
        when: "I access the GWELLS administration feature"
        then: "I can add a survey where required."
     }
}