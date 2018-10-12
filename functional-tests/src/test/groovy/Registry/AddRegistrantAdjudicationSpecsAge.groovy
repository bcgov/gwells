import geb.spock.GebReportingSpec
import spock.lang.*

@Title("Register of Well Drillers and Well Pump Installers - Add Registrant - Adjudication")
@Narrative("""As an authorized user, I need to be able to document that an applicant for registration as a 
well driller and well pump installer meets the age requirement specified under the GWPR.""")
@See("https://trello.com/c/YdYXQLw8")
class AddRegistrantAdjudicationSpecsAge extends GebReportingSpec {

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/YdYXQLw8")
    def "Scenario: 1 - Drop Down"(){
        given "that I am an adjudicator or statutory authority"
        when "I am reviewing an application for registration"
        and "I have confirmed that the applicant is 19 years of age or older"
	    then "I must select a value from the proof of age drop down."
    }

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/vYd6OvhV")
    def "Scenario: 2 - Drivers,Passport & Birth Certificate"(){
        given "that I am an adjudicator or statutory authority"
        and "I have confirmed that the applicant is 19 years of age or older"
	    then "proof of age values must include driver's licence, passport, birth certificate."
     }

}
