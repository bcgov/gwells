import geb.spock.GebReportingSpec
import spock.lang.*

@Title("Create an Application Maintenance error message")
@Narrative("""As an admin, I need a setting which shows the site is down for maintenance when I am doing activities like upgrades 
and database refreshes so that users know the site isn't broken and will be available again shortly.""")
@See("https://trello.com/c/qfhKDGxY")
class AppMaintenanceSpecs extends GebReportingSpec {

    @Unroll
    @Ignore("TODO")
    @Issue("https://trello.com/c/qfhKDGxY")
    def "Scenario: 1 - Verify Application Maintenance error message"(){
        given "I am an application Administrator"
        and "maintenance activities need to occur that will affect the public site"
        when "the public application is down"
        then "an error message is displayed to users indicating 'Site is currently down for maintenance and will be back up shortly'."
     }
}