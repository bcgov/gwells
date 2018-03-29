import geb.spock.GebReportingSpec
import pages.app.HomePage
import pages.app.RegisterPage
import pages.app.SearchPage
import pages.app.AdditionalInformationPage
import pages.app.WellDrillerPage
import pages.external.Accessibility
import pages.external.Copyright
import pages.external.Disclaimer
import pages.external.Privacy
import pages.external.BCWaterResourceAtlas
import pages.external.iMapBC
import pages.external.AboutGov
import pages.external.GovHome
import spock.lang.*

@Title("Basic Navigational Tests")
@Narrative("""As a user I expect all links in the GWELLS application to work.""")
class FlowSpecs extends GebReportingSpec {

    @Unroll
    def "Navigate Page from: #startPage, click Link: #clickLink, Assert Page: #assertPage"(){
	    given: "I start on the #startPage"
			to startPage
        when: "I click on the link #clickLink"
			waitFor { $("a", id:"$clickLink").click() }
        then:
			at assertPage

        where:
        startPage                   | clickLink                | clickCount    | timeoutSeconds    || assertPage
        SearchPage                  | "ribbon-groundwaterinfo" | 1             | 3                 || AdditionalInformationPage
        AdditionalInformationPage   | "ribbon-search"          | 1             | 3                 || SearchPage
        SearchPage    		        | "ribbon-search"          | 1             | 3                 || SearchPage
        SearchPage                  | "BCWRAtlas"              | 1             | 3                 || BCWaterResourceAtlas
        SearchPage                  | "iMapBC"                 | 1             | 3                 || iMapBC
        SearchPage                  | "ribbon-registry-legacy" | 1             | 3                 || WellDrillerPage
        //Test Externally Linked Pages
		SearchPage           | "footer-disclaimer"     | 1             | 3                 || Disclaimer
        SearchPage           | "footer-privacy"        | 1             | 3                 || Privacy
        SearchPage           | "footer-accessibility"  | 1             | 3                 || Accessibility
        SearchPage           | "footer-copyright"      | 1             | 3                 || Copyright
        SearchPage           | "footer-home"           | 1             | 3                 || GovHome
        SearchPage           | "footer-about"          | 1             | 3                 || AboutGov
    }

    def "Check Registries Page"(){
        given: "I go to the registries start page"
            to RegisterPage
        when: "I am on the page"    
            at RegisterPage
        then: "title = 'Register of Well Drillers and Well Pump Installers'" 
            assert titletext == "Register of Well Drillers and Well Pump Installers"   
    }
}
