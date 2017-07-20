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
			$("a", text:"$clickLink").click()
        then:
			at assertPage
		
		
        where:
        startPage           | clickLink                     | clickCount    | timeoutSeconds    || assertPage
        HomePage       		| "Search"                      | 1             | 3                || SearchPage
        
        //Test Externally Linked Pages
        HomePage      | "Copyright"        | 1             | 3                 || Copyright
        // These external tests are not currently working
		//HomePage      | "Disclaimer"       | 1             | 3                 || Disclaimer
        //HomePage      | "Privacy"          | 1             | 3                 || Privacy
        HomePage      | "Accessibility"    | 1             | 3                 || Accessibility
    }
}
