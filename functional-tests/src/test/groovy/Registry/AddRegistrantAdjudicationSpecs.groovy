import geb.spock.GebReportingSpec
import spock.lang.*

@Title("Register of Well Drillers and Well Pump Installers - Add Registrant - Adjudication")
@Narrative("""As an authorized user, I need to be able to track the adjudication process related to a well
driller or well pump installer within the registers in order to facilitate better management and processing
of applications.""")
@See("https://trello.com/c/vYd6OvhV")
class AddRegistrantAdjudicationSpecs extends GebReportingSpec {

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/vYd6OvhV")
    def "Scenario: 1 - Show"(){
        given "given that I am an adjudicator or statutory authority"
        and "I need to add another classification"
       	when "I select the box 'add new classification'"
       	then "a new classification and qualifications and adjudication section should appear."
     }

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/vYd6OvhV")
    def "Scenario: 2 - Pending"(){
        given "given that I am an adjudicator or statutory authority"
        when "I have entered date application received"
       	then "register status should be defaulted to 'pending'."
     }

}
