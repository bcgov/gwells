import geb.spock.GebReportingSpec
import spock.lang.*

@Title("Register of Well Drillers and Well Pump Installers - Manage Companies")
@Narrative("""As an authorized user, I want to be able to update or remove company contact information
associated with the well driller and well pump installer registers to ensure that the company contact
information is up-to-date.""")
@See("https://trello.com/c/JESPCA7k")
class EditCompanySpecs extends GebReportingSpec {

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/JESPCA7k")
    def "Scenario: 1 - Add company"(){
	given "that I am an adjudicator or statutory authority"
    and "I need to add a new company to the list of companies"
	when "I select the 'add new company' button"
	then "an empty screen for company information is displayed."
     }
    
    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/JESPCA7k")
    def "Scenario: 2 - Select Company"(){
    given "that I am the adjudicator or statutory authority" 
    and "I want to search for an existing company to update their contact information" 
	when "I select a company name from the company name dropdown menu" 
	then "that company information should be displayed in the company information section." 
     }

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/JESPCA7k")
    def "Scenario: 3 - Delete company"(){
 	given "that I am the adjudicator or statutory authority" 
    and "I have accidentally entered a company twice"
	when "I select the 'Delete' button"  
	then "I a popup message should be displayed asking me to confirm deletion and warning if there are individuals associated to this company." 
     }
}
