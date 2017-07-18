import geb.spock.GebReportingSpec
import pages.app.HomePage
import pages.app.SearchPage
import pages.external.Accessability
import pages.external.Copyright
import pages.external.Disclaimer
import pages.external.Privacy
import spock.lang.Unroll

class FlowSpecs extends GebReportingSpec {

    @Unroll
    def "Navigate Page from: #startPage, click Link: #clickLink, Assert Page: #assertPage"(){
        when:
        to startPage

        and:
        (1..clickCount).each{
            $("a", id:"$clickLink").click()
        }

        then:
        at assertPage

        where:
        startPage           | clickLink                     | clickCount    | timeoutSeconds    || assertPage
        HomePage       | "navbar-notifications"        | 1             | 3                 || NotificationsPage
        SettingsPage        | "navbar-notifications"        | 1             | 3                 || NotificationsPage
        NotificationsPage   | "navbar-settings"             | 1             | 3                 || SettingsPage

        //Test Externally Linked Pages
        HomePage      | "footer-about-copyright"        | 1             | 3                 || Copyright
        HomePage      | "footer-about-disclaimer"       | 1             | 3                 || Disclaimer
        HomePage      | "footer-about-privacy"          | 1             | 3                 || Privacy
        HomePage      | "footer-about-accessibility"    | 1             | 3                 || Accessability
    }
}
