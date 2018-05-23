import geb.spock.GebReportingSpec
import spock.lang.*

@Title("Register of Well Drillers and Well Pump Installers - Add Registrant - Classification and Qualifications")
@Narrative("""As an authorized user, I need to be able to track the classification and qualification
information related to a well driller or well pump installer within the registers in order to facilitate
better management and processing of applications.""")
@See("https://trello.com/c/5xbTW0Fz")
class AddRegistrantClassificationQualificationsSpecs extends GebReportingSpec {

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/5xbTW0Fz")
    def "Scenario: 1 - Show"(){
        given "that I am an adjudicator or statutory authority"
	    when "I select the 'Add new classification' button"
        then "the Classification and Qualifications section should expand to show me the data entry fields and adjudication section."
     }

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/5xbTW0Fz")
    def "Scenario: 2 - Select"(){
        given "that I am an adjudicator or statutory authority"
       	when "I select the appropriate classification"
       	then "I should only be allowed to select one classification at a time."
     }

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/5xbTW0Fz")
    def "Scenario: 3 - Show"(){
        given "that I am an adjudicator or statutory authority"
        when "I select the certification issued by drop down menu"
        then "I should get options based specific to whether the classification is for a well driller (water well, geotechnical/evironmental, geoexchange) or a well pump installer."
     }

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/5xbTW0Fz")
    def "Scenario: 4 - Multiple"(){
        given "that I am an adjudicator or statutory authority"
       	when "I select the 'Add additional certification' button"
       	then "a new certification issued by dropdown menu and certificate number field should be displayed"
     }

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/5xbTW0Fz")
    def "Scenario: 5 - Checkboxes"(){
        given "that I am an adjudicator or statutory authority"
       	when "I select the classification of water well driller"
       	then "the appropriate qualified to drill check boxes get automatically populated"
        and "I have the ability to override those check boxes."
     }

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/5xbTW0Fz")
    def "Scenario: 6 - Auto select"(){
        given "that I am an adjudicator or statutory authority"
       	when "I select the classification of water well driller"
       	then "the following check boxes are selected: water supply well, monitoring well, recharge well, injection well, dewatering well, remediation well, geotechnical well."
     }

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/5xbTW0Fz")
    def "Scenario: 7 - Auto select"(){
        given "that I am an adjudicator or statutory authority"
       	when "I select the classification of geotechnical/environmental driller"
       	then "the following check boxes are selected: monitoring well, remediation well, geotechnical well."
     }

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/5xbTW0Fz")
    def "Scenario: 8 - Auto select"(){
        given "given that I am an adjudicator or statutory authority"
       	when "I select the classification of geoexchange driller"
       	then "the following check boxes are selected: closed-loop geoexchange well."
     }
}
