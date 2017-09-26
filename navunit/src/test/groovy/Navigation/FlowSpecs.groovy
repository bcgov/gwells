import geb.spock.GebReportingSpec
import pages.app.HomePage
import pages.app.SearchPage
import pages.app.AdditionalInformationPage
import pages.external.Accessibility
import pages.external.Copyright
import pages.external.Disclaimer
import pages.external.Privacy
import pages.external.BCWaterResourceAtlas
import pages.external.iMapBC
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
        startPage                   | clickLink                | clickCount    | timeoutSeconds    || assertPage
        HomePage                    | "ribbon-home"            | 1             | 3                 || HomePage
        HomePage                    | "ribbon-additionalinfo"  | 1             | 3                 || AdditionalInformationPage
        AdditionalInformationPage   | "ribbon-home"            | 1             | 3                 || HomePage
        HomePage       		        | "ribbon-search"          | 1             | 3                 || SearchPage
        SearchPage    		        | "ribbon-home"            | 1             | 3                 || HomePage
        SearchPage                  | "BCWRAtlas"              | 1             | 3                 || BCWaterResourceAtlas
        SearchPage                  | "iMapBC"                 | 1             | 3                 || iMapBC
                
        //Test Externally Linked Pages
		HomePage            | "footer-disclaimer"     | 1             | 3                 || Disclaimer
        HomePage            | "footer-privacy"        | 1             | 3                 || Privacy
        HomePage            | "footer-accessibility"  | 1             | 3                 || Accessibility
        HomePage            | "footer-copyright"      | 1             | 3                 || Copyright
    }
}
