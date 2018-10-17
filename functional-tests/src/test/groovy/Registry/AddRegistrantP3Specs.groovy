import geb.spock.GebReportingSpec
import spock.lang.*

@Title("Register of Well Drillers and Well Pump Installers - Add Registrant Part 3")
@Narrative("""As a Groundwater Data Specialist and person assigned to manage the register of well drillers and well pump installers for the comptroller, 
I need a tool to add new registrant information into the register of well drillers or well pump 
installers in order to facilitate better management and processing of applications and applicant information.""")
@See("https://trello.com/c/NYH7yqyJ")
class AddRegistrantP3Specs extends GebReportingSpec {

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/NYH7yqyJ")
    def "Scenario: 1 - Save Application"(){
       	given "that I am an authorized user"
        and "I have entered all the required information from the application"
        when "I select 'Save'"
        then "the record is saved to the database."
     }

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/NYH7yqyJ") 
    def "Scenario: 2 - Cancel Application"(){
       	given "that I am an authorized user"
        and "I have entered all the required information from the application"
        when "I select 'Cancel'"
        then "a pop-up is displayed confirming that I do in fact want to cancel the record without saving."
     }
}
