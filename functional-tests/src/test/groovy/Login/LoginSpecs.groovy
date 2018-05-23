import geb.spock.GebReportingSpec
import spock.lang.*
import pages.app.RegisterPage
import pages.external.SSO

@Title("Login")
@Narrative("""As an authorized groundwater staff, I need a log in link in order to have access to files (e.g., the well driller registry, edit) 
in order to CRUD my applicable records.""")
@See("https://trello.com/c/Uz8PvC8k")
class LoginSpecs extends GebReportingSpec {

    @Ignore("TODO")
    @Issue("https://trello.com/c/Uz8PvC8k")
    def "Scenario: 1 - Show Login"(){
        given: "that I am a GWELLS user"
        when: "I open the GWELLS application"
        then: "I should see a sign in link at the top right of the navigation bar."
     }

    @Ignore("SSO will not accept redirects from our test instances")
    @Issue("https://trello.com/c/Uz8PvC8k")
    def "Scenario: 2 - Login"(){
        given: "that I am an an authorized GWELLS user"
            to RegisterPage
        when: "I select the sign in link at the top right if the navigation bar"
            waitFor { $("#gwells-sso-login").click() }
        then: "I should sign in using my IDIR."
            at SSO
     }

    @Ignore("TODO")
    @Issue("https://trello.com/c/Uz8PvC8k")
    def "Scenario: 3 - Login Unauthorized"(){
        given: "that I am an unauthorized GWELLS user"
        when: "I select the sign in link at the top right if the navigation bar"
        then: "I should be directed to the 301 error message page."
     }     
}