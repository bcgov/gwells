import geb.spock.GebReportingSpec
import pages.app.HomePage
import pages.app.ActivitySubmissionPage
import pages.external.Accessibility
import pages.external.Copyright
import pages.external.Disclaimer
import pages.external.Privacy
import spock.lang.Unroll


class ActivitySubmissionDefaultSpec extends GebReportingSpec {

    @Unroll
    def "Should default to Construction Report when enter new report clicked from home page"() {
        given:
        to HomePage

        when:
        $("a", id:"enterNewReport").click()

        then:
		at ActivitySubmissionPage

        and:
        $("input[name='type_and_class-well_activity_type']:checked").closest("label").text() == "Construction"
    }
}
