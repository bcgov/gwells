import geb.spock.GebReportingSpec
import spock.lang.*

@Title("Register of Well Drillers and Well Pump Installers - Add Registrant Part 2")
@Narrative("""As a Groundwater Data Specialist and person assigned to manage the register of well drillers and well pump installers for the comptroller, 
I need a tool to add new registrant information into the register of well drillers or well pump installers in order to facilitate better management and 
processing of applications and applicant information.""")
@See("https://trello.com/c/JESPCA7k")
class AddRegistrantP2Specs extends GebReportingSpec {

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/JESPCA7k")
    def "Scenario: 1 - Registration/Approval Error"(){
       	given "that I am an authorized user"
        and "the registration status is set to 'Registered'"
        and "the approval outcome is set to 'Approved'"
        when "I save the record"
        and "I have not entered an approval outcome date and/or registration number"
        then "I should get an error message at the top of the page stating 'Approval date required' OR 'Registration Number Required'."
     }
    
    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/JESPCA7k")
    def "Scenario: 2 - Select 'Well Driller'"(){
       	given "that I am an authorized user"
        and "I have a new application for registration as a well driller to be entered into the system"
        and "the type of applicant selected is 'well driller'"
        when "I view the data entry page"
        and "I have not entered an approval outcome date and/or registration number"
        then "I should see the data entry section related to 'Driller Qualifications'."
     }

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/JESPCA7k")
    def "Scenario: 3 - No driller qualification selected"(){
       	given "that I am an authorized user"
        and "I have a new application for registration as a well driller or well pump installer to be entered into the system"
        and "the registration status is set to 'Registered'"
        and "the approval outcome is set to 'Approved'"
        when "I save the record"
        and "I have not selected at least one check box under qualified to drill"
        then "I should get an error message at the top of the page stating 'At least one driller qualification must be selected'."
     }
}
