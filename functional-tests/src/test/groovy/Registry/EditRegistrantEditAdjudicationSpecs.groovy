import geb.spock.GebReportingSpec
import spock.lang.*

@Title("Register of Well Drillers and Well Pump Installers - Edit Registrant - Classification and Qualifications - Adjudication")
@Narrative("""As a Groundwater Data Specialist and person assigned to manage the register of well drillers and well pump installers for the comptroller, I need to be able to edit an individuals file related to their registration as a well driller or well pump installer in order to ensure their information is up to date and meets the requirements of the Groundwater Protection Regulation.
This story excludes functionality relating to the removal from the register.
""")
@See("https://trello.com/c/zaa4JSn8")
class AddRegistrantEditAdjudicationSpecs extends GebReportingSpec {

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/zaa4JSn8")
    def "Scenario: 1 - Save"(){
        given "that I am an authorized user"
	    when "I save the record"
        then "all my changes will be saved"
     }

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/zaa4JSn8")
    def "Scenario: 2 - Cancel"(){
        given "that I am an authorized user"
       	when "I cancel before saving the record"
       	then "a popup message should be displayed confirming that I want to cancel."
     }

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/zaa4JSn8")
    def "Scenario: 3 - Select"(){
        given "that I am an authorized user"
        when "I enter an approval outcome date"
        then "approval outcome must be selected."
     }

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/zaa4JSn8")
    def "Scenario: 4 - Reason"(){
        given "that I am an authorized user"
       	when "I enter an approval outcome of not approved"
       	then "reason not approved must be completed."
     }

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/zaa4JSn8")
    def "Scenario: 5 - Publish"(){
        given "that I am an authorized user"
       	when "I enter an approval outcome of approved"
       	then "the record must be publicaly published on the register search page."
     }
}
