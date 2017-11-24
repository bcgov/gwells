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
			go "gwells/well/$WellId"
 		when: "I accessed the Well Summary Page"	
			at WellSummaryPage
			assert  (well_tag_number.text() == "$WellId")
        then: "Then I see all available information related to the well"
        	at WellSummaryPage
			assert summary_information
			assert well_tag_number
			assert identification_plate_number
			assert owner_full_name
			assert licenced_status
			assert well_well_status
			assert well_class
			assert well_subclass
			assert intended_water_use
			assert obs_well_number
			assert obs_well_status
			assert ems_id
			assert aquifer_number
			assert alternate_specs_submitted
			assert water_supply_system_name
			assert water_supply_system_well_name

			assert address
			assert city
			assert legal
			assert lot
			assert plan
			assert district_lot
			assert block
			assert section
			assert township
			assert range
			assert land_district
			assert pid

			assert location_desc
			assert latitude
			assert longitude
			assert utm_zone_code
			assert utm_northing
			assert utm_easting
			assert utm_accuracy_code
			assert bcgs_mapsheet_number

			assert activities
			assert construction_end_date
			assert alteration_end_date
			assert decommission_end_date
			assert drilling_company

			assert total_depth_drilled
			assert static_water_level
			assert well_cap_type
			assert finished_well_depth
			assert well_yield
			assert well_disinfected
			assert final_casing_stickup
			assert artesian_flow
			assert drilling_method
			assert bedrock_depth
			assert artesian_pressure
			assert orientation_direction
			assert ground_elevation
			assert ground_elevation_method
			assert well_plate_attached

			assert intake_method
			assert screen_type
			assert screen_material
			assert screen_opening
			assert screen_bottom
			assert screens

			assert developed_by
			assert devlopment_total_duration

			assert yield_estimation_method
			assert yield_estimation_rate
			assert yield_estimation_duration

			assert casing_field_set
			assert casings

			assert surface_seal_fieldset
			assert surface_seal_method
			assert surface_seal_material
			assert surface_seal_thickness
			assert surface_seal_length
			assert backfill_type
			assert backfill_depth

			assert perforations_fieldset
			assert liner_details

			assert well_tag_number_link
        where:
        TestDesc                          | WellId           
        "Well Tag - 21265"                    | 21265
    } 
    @Unroll

    def "Field content checking: #TestDesc - #WellId - #WellFieldContent"() {
        given: "Given that I have found my well"
			go "gwells/well/$WellId" 
 	 	when: "I accessed the Well Summary Page"	
			at WellSummaryPage
        then: "Then I see the expected information for the #TestDesc"
			at WellSummaryPage
			println "$TestDesc: " +  page."$TestDesc".text().trim()
			assert page."$TestDesc".text().trim() == "$WellFieldContent".trim()
		where:	
        TestDesc                          | WellFieldContent 	| WellId           
		"well_tag_number"				  | "48084" 			| 48084
		"identification_plate_number"     | "13297" 			| 48084
		"owner_full_name"				  | "RICK PIPES"		| 48084
		"licenced_status"				  | "Unlicensed"		| 48084
		"well_well_status"				  | "New"				| 48084
		"well_class"	 | "Water Supply" 	 | 48084
		"well_subclass"	 | "Domestic" 	 | 48084
		"intended_water_use"	 | "Water Supply System" 	 | 48084
		"obs_well_number"	 | "2" 	 | 26787
		"obs_well_status"	 | "Active" 	 |  26787
		"ems_id"	 | "1401057" 	 | 26787
		"aquifer_number"	 | "207" 	 | 48084
		"alternate_specs_submitted"	 | "No" 	 | 48084
		"water_supply_system_name"	 | "LA POMMERAI: MERRIDALE CIDERWORKS" 	 | 48084
		"water_supply_system_well_name"	 | "PRODUCTION WELL" 	 | 48084
		"address"	 | "1230 MERRIDALE ROAD" 	 | 48084
		"city"	 | "COBBLE HILL" 	 | 48084
		"lot"	 | "B" 	 | 48084
		"plan"	 | "220658" 	 | 48084
		"district_lot"	 | "405" 	 | 110749
		"block"	 | "9" 	 | 18624
		"section"	 | "5" 	 | 48084
		"township"	 | "16" 	 | 26787
		"range"	 | "6" 	 | 48084
		//"land_district"	 | "" 	 | 
		"pid"	 | "8048142" 	 | 110749
		"location_desc"	 | "PREVIOUS LEGAL PLAN: 14144" 	 | 110749
		"latitude"	 | "48.663734" 	 | 48084
		"longitude"	 | "-123.585250" 	 | 48084
		"utm_zone_code"	 | "10" 	 | 48084
		"utm_northing"	 | "5390241" 	 | 48084
		"utm_easting"	 | "456906" 	 | 48084
		"utm_accuracy_code"	 | "H" 	 | 48084
		"bcgs_mapsheet_number"	 | "092B063313" 	 | 48084
		"construction_end_date"	 | "1976-01-29" 	 | 110749
		"alteration_end_date"	 | "2014-11-23" 	 | 110749
		"decommission_end_date"	 | "2014-11-23" 	 | 110749
		"drilling_company"	 | "A. D. Baker Drilling" 	 | 48084
		"total_depth_drilled"	 | "275.00 feet" 	 | 48084
		//"static_water_level"	 | "" 	 | 
		//"well_cap_type"	 | "" 	 | 
		"finished_well_depth"	 | "275.00 feet" 	 | 48084
		"well_yield"	 | "40.000 GPM" 	 | 48084
		"well_disinfected"	 | "False" 	 | 48084
		//"final_casing_stickup"	 | "" 	 | 
		"artesian_flow"	 | "15.00 USGM" 	 | 110749
		"drilling_method"	 | "AIR_ROTARY" 	 | 48084
		"bedrock_depth"	 | "43.00 feet" 	 | 48084
		//"artesian_pressure"	 | "" 	 | 
		"orientation_direction"	 | "vertical" 	 | 48084
		"ground_elevation"	 | "193.10 feet" 	 | 26787
		"ground_elevation_method"	 | "Differential GPS" 	 | 26787
		"well_plate_attached"	 | "CASING" 	 | 48084
		"intake_method"	 | "Open Bottom" 	 | 110749
		//"screen_type"	 | "" 	 | 
		//"screen_material"	 | "" 	 | 
		//"screen_opening"	 | "" 	 | 
		//"screen_bottom"	 | "" 	 | 
		"developed_by"	 | "Bailing" 	 | 110749
		"devlopment_total_duration"	 | "3.00 hours" 	 | 110749
		//"yield_estimation_method"	 | "" 	 | 
		"yield_estimation_rate"	 | "15.00   USGM" 	 | 110749
		"yield_estimation_duration"	 | "12.00   hours" 	 | 110749
		//"surface_seal_fieldset"	 | "" 	 | 
		//"surface_seal_method"	 | "" 	 | 
		//"surface_seal_material"	 | "" 	 | 
		//"surface_seal_thickness"	 | "" 	 | 
		"surface_seal_length"	 | "15.00" 	 | 110749
		//"backfill_type"	 | "" 	 | 
		//"backfill_depth"	 | "" 	 |  
    } 	
}
