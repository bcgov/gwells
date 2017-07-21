import geb.spock.GebReportingSpec
import pages.app.HomePage
import pages.app.SearchPage
import pages.external.Accessibility
import pages.external.Copyright
import pages.external.Disclaimer
import pages.external.Privacy
import spock.lang.Unroll


class FlowSpecs extends GebReportingSpec {

    @Unroll
    def "Navigate Page from: #startPage, click Link: #clickLink, Assert Page: #assertPage"(){
	    given: "I start on the #startPage"
			to startPage
        when: "I click on the link #clickLink"
			$("a", id:"$clickLink").click()
        then:
			at assertPage
		
		
        where:
        startPage           | clickLink                     | clickCount    | timeoutSeconds    || assertPage
        HomePage       		| "ribbon-search"               | 1             | 3                 || SearchPage
        HomePage            | "navbar-search"               | 1             | 3                 || SearchPage
        SearchPage    		| "ribbon-home"                 | 1             | 3                 || HomePage
        SearchPage          | "navbar-home"                 | 1             | 3                 || HomePage
        
        //Test Externally Linked Pages
		HomePage            | "footer-disclaimer"     | 1             | 3                 || Disclaimer
        HomePage            | "footer-privacy"        | 1             | 3                 || Privacy
        HomePage            | "footer-accessibility"  | 1             | 3                 || Accessibility
        HomePage            | "footer-copyright"      | 1             | 3                 || Copyright
    }
}
