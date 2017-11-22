import geb.spock.GebReportingSpec
import pages.app.SearchPage
import pages.app.WellSummaryPage

import spock.lang.Ignore
import spock.lang.Issue
import spock.lang.Narrative
import spock.lang.See
import spock.lang.Specification
import spock.lang.Title
import spock.lang.Unroll

@Title("Well Details")
@Narrative("""
As a general public user, I need to be able to access a summary report, 
through Search,  and see relevant information related to my well of interest.
""")
class WellDetailsSpecs extends GebReportingSpec {
    @Unroll

    def "Basic Field availability checking: #TestDesc"() {
        given: "Given that I have found my well"
			to SearchPage
 			SearchWell("$WellId", "","","")
 		when: "I accessed the Well Summary Page"	
			$('#results > tbody > tr:nth-child('+ ReturnRow("$WellId").toString() +') > td.sorting_1 > a').click()
			at WellSummaryPage
			assert  (well_tag_number.text() == "$WellId")
        then: "Then I see all available information related to the well"
        	at WellSummaryPage
			assert activitiesTable
			assert address 
			assert alteration_end_date
			assert alternate_specs_submitted 
			assert aquifer_number
			assert block 
			assert casingsTable 
			assert city 
			assert construction_end_date
			assert decommission_end_date
			assert district_lot 
			assert drilling_company 
			assert ems_id 
			assert finished_well_depth 
			assert identification_plate_number 
			assert intended_water_use 
			assert land_district 
			assert latitude 
			assert legalTable 
			assert licenced_status 
			assert location_desc 
			assert longitude 
			assert lot 
			assert obs_well_number 
			assert obs_well_status 
			assert owner_full_name 
			assert pid 
			assert plan 
			assert range 
			assert screen_bottom
			assert screen_material
			assert screen_opening
			assert screen_type
			assert screensTable 
			assert section 
			assert static_water_level 
			assert total_depth_drilled 
			assert township 
			assert well_cap_type 
			assert well_class 
			assert well_disinfected 
			assert well_plate_attached 
			assert well_subclass 
			assert well_tag_number
			assert well_well_status 
			assert well_yield 
			assert yield_estimation_duration 
			assert yield_estimation_method
			assert yield_estimation_rate
        where:
        TestDesc                          | WellId           
        "Well Tag - 21265"                    | 21265
    } 
}
