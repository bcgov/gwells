import geb.spock.GebReportingSpec
import spock.lang.*

@Title("Register of Well Drillers and Well Pump Installers - Add Registrant Part 1")
@Narrative("""As a Groundwater Data Specialist and person assigned to manage the register of well drillers and well pump installers for the comptroller, 
I need a tool to add new registrant information into the register of well drillers or well pump installers in order to facilitate better management and 
processing of applications and applicant information.""")
@See("https://trello.com/c/rtIOyw84")
class AddRegistrantP1Specs extends GebReportingSpec {

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/rtIOyw84")
    def "Scenario: 1 - Applicant type selection Error"(){
       	given "that I am an authorized user"
        and "I have a new application for registration as a well driller or well pump installer to be entered into the system"
        when "I save the record"
        and "I have not selected the type of applicant"
        then "I should get an error message at the top of the page stating 'Type of applicant must be selected'."
     }

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/rtIOyw84")
    def "Scenario: 2 - Applicant Last name Error"(){
       	given "that I am an authorized user"
        and "I have a new application for registration as a well driller or well pump installer to be entered into the system"
        when "I save the record"
        and "I have not entered the last name of the applicant"
        then "I should get an error message at the top of the page stating 'Last name must be completed'"
     }

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/rtIOyw84")
    def "Scenario: 2 - Applicant First name Error"(){
       	given "that I am an authorized user"
        and "I have a new application for registration as a well driller or well pump installer to be entered into the system"
        when "I save the record"
        and "I have not entered the first name of the applicant"
        then "I should get an error message at the top of the page stating 'Last name must be completed'."
     }

}
