import geb.spock.GebReportingSpec
import geb.Browser
import pages.app.SearchPage
import pages.app.WellSummaryPage
import pages.external.AquiferReport

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
    def "Basic Field availability checking: #TestDesc #WellId"() {
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
			assert no_liner_details_information

			assert lithology_fieldset
			assert lithology

			assert well_decommissioning
        	assert reason_for_decommission
        	assert method_of_closure
        	assert decommission_details

			assert comments
			//assert no_document_msg

        where:
        TestDesc                          | WellId
        "Well Tag - "                    | 110749
    }

    @Unroll
    def "Basic Field availability checking liner details: #TestDesc #WellId"() {
        given: "Given that I have found my well that has liner details"
			go "gwells/well/$WellId"
 		when: "I accessed the Well Summary Page"
			at WellSummaryPage
			assert  (well_tag_number.text() == "$WellId")
        then: "Then I see all the liner details related to the well"
        	at WellSummaryPage

        assert liner_details_table

        where:
        TestDesc                          | WellId
        "Well Tag - "                    | 108027
      }

    @Unroll
    def "Basic Field availability checking screen details: #TestDesc #WellId"() {
        given: "Given that I have found a well with screen details"
			go "gwells/well/$WellId"
 		when: "I accessed the Well Summary Page"
			at WellSummaryPage
			assert  (well_tag_number.text() == "$WellId")
        then: "Then I see all screen details related to the well"
        	at WellSummaryPage

        assert screens

        where:
        TestDesc                          | WellId
        "Well Tag - "                    | 108025
      }

    @Unroll
    def "Basic Field availability checking screen details: #TestDesc #WellId"() {
        given: "Given that I have found a well without screen details"
      go "gwells/well/$WellId"
    when: "I accessed the Well Summary Page"
      at WellSummaryPage
      assert  (well_tag_number.text() == "$WellId")
        then: "Then I see a notice that tells me there is no screen information for that well"
          at WellSummaryPage

        assert no_screen_information

        where:
        TestDesc                          | WellId
        "Well Tag - "                    | 104671
      }

    @Unroll
    def "Basic Field availability checking casing details: #TestDesc #WellId"() {
        given: "Given that I have found a well with casing details"
			go "gwells/well/$WellId"
 		when: "I accessed the Well Summary Page"
			at WellSummaryPage
			assert  (well_tag_number.text() == "$WellId")
        then: "Then I see all casing details related to the well"
        	at WellSummaryPage

        assert casings

        where:
        TestDesc                          | WellId
        "Well Tag - "                    | 108025
      }

    @Unroll
    def "Basic Field availability checking casing details: #TestDesc #WellId"() {
        given: "Given that I have found a well without casing details"
      go "gwells/well/$WellId"
    when: "I accessed the Well Summary Page"
      at WellSummaryPage
      assert  (well_tag_number.text() == "$WellId")
        then: "Then I see a notice that tells me there is no casing information for that well"
          at WellSummaryPage

        assert no_casing_information

        where:
        TestDesc                          | WellId
        "Well Tag - "                    | 104671
      }


      @Unroll
      def "Basic Field availability checking lithology details: #TestDesc #WellId"() {
          given: "Given that I have found a well with lithology details"
  			go "gwells/well/$WellId"
   		when: "I accessed the Well Summary Page"
  			at WellSummaryPage
  			assert  (well_tag_number.text() == "$WellId")
          then: "Then I see all lithology details related to the well"
          	at WellSummaryPage

          assert lithology

          where:
          TestDesc                          | WellId
          "Well Tag - "                    | 105747
        }

      @Unroll
      def "Basic Field availability checking lithology details: #TestDesc #WellId"() {
          given: "Given that I have found a well without lithology details"
        go "gwells/well/$WellId"
      when: "I accessed the Well Summary Page"
        at WellSummaryPage
        assert  (well_tag_number.text() == "$WellId")
          then: "Then I see a notice that tells me there is no lithology information for that well"
            at WellSummaryPage

          assert no_lithology_information

          where:
          TestDesc                          | WellId
          "Well Tag - "                    | 104671
        }

    @Unroll
    def "Field content checking: #TestDesc - #WellId - #WellFieldContent"() {
        given: "Given that I have found my well"
			go "gwells/well/$WellId"
 	 	when: "I accessed the Well Summary Page"
			at WellSummaryPage
        then: "Then I see the expected information(#WellFieldContent) for the #TestDesc field"
			at WellSummaryPage
			//println "$TestDesc: " +  page."$TestDesc".text().trim()
			//assert page."$TestDesc".text().trim() == "$WellFieldContent".trim()
		where:
        TestDesc                          | WellFieldContent 	| WellId
		"well_tag_number"				  | "110749" 			| 110749
		"identification_plate_number"     | "47948" 			| 110750
		"owner_full_name"				  | "ROYAL CANADIAN MOUNTED POLICE"		| 110749
		"licenced_status"				  | "UNLICENSED"		| 110749
		"well_well_status"				  | "CLOSURE"			| 110749
		"well_class"	 				  | "Water Supply" 	 | 110749
		"well_subclass"	 				  | "Domestic" 	 | 110749
		"intended_water_use"	 		  | "Water Supply System" 	 | 110749
		"obs_well_number"	 			  | "402" 	 | 102364
		//"obs_well_number"	 			  | "179" 	 | 4980 //no link
		"obs_well_status"	    		  | "Active" 	 |  102364
		"ems_id"	 					  | "E283990" 	 | 102364
		"aquifer_number"	 			  | "936" 	 | 102364
		//"aquifer_number"	 			  | "464" 	 | 4980 //no link
		"alternate_specs_submitted"	 	  | "No" 	 | 110749
		//"water_supply_system_name"	 	  | "CHETWYND PULP MILL" 	 | 102406
		//"water_supply_system_well_name"	  | "EAST WELL" 	 | 102406
		"address"	 					  | "6647 CHRISTENSEN ROAD" 	 | 110749
		"city"	 						  | "ANAHIM LAKE" 	 | 110749
		"lot"							  | "A" 	 | 110749
		"plan"							  | "25014" 	 | 110749
		"district_lot"	 				  | "405" 	 | 110749
		"block"	 						  | "19" 	 | 100127
		"section"	 					  | "28" 	 | 100542
		"township"	 					  | "21" 	 | 100500
		"range"	 						  | "3" 	 | 110749
		"land_district"	 				  | "26 KOOTENAY" 	 | 110750
		"pid"	 						  | "008048142" 	 | 110749
		"location_desc"	 				  | "PREVIOUS LEGAL PLAN: 14144" 	 | 110749
		"latitude"	 					  | "52.465449" 	 | 110749
		"longitude"	 					  | "-125.300830" 	 | 110749
		"utm_zone_code"	 				  | "10" 	 | 110749
		"utm_northing"	 				  | "5815298" 	 | 110749
		"utm_easting"	             	  | "343701" 	 | 110749
		"utm_accuracy_code"	 			  | "H" 	 | 110749
		"bcgs_mapsheet_number"	 		  | "093C044324" 	 | 110749
		"construction_end_date"	          | "1976-01-29" 	 | 110749
		"alteration_end_date"	 		  | "2014-11-23" 	 | 110749
		"decommission_end_date"	 		  | "2014-11-23" 	 | 110749
		"drilling_company"	  			  | "Industrial Drillers" 	 | 110749
		"total_depth_drilled"	 		  | "285 feet" 	 | 110749
		"static_water_level"	 		  | "128 feet" 	 | 106648
		"well_cap_type"	   				  | "VENT CAST" 	 | 106648
		"finished_well_depth"	 		  | "100 feet" 	 | 105747
		"well_yield"	 				  | "15 USGPM" 	 | 110749
		"well_disinfected"	 			  | "No" 	 | 110749
		"final_casing_stickup"	 		  | "12 inches" 	 | 106648
		"artesian_flow"	 				  | "15 USGPM" 	 | 110749
		"drilling_method"	 			  | "AIR_ROTARY" 	 | 100501
		"bedrock_depth"	 				  | "60 feet" 	 | 110749
		"artesian_pressure"	    		  | "11 inches" 	 | 113552
		"orientation_direction"	 		  | "vertical" 	 | 110749
		"ground_elevation"	 			  | "378 feet" 	 | 106648
		"ground_elevation_method"	 	  | "1:10,000 Scale Map" 	 | 104636
		//"well_plate_attached"	 		  | "CASING" 	 | 106648
		// "intake_method"	 				  | "Open Bottom" 	 | 110749
		"screen_type"	 				  | "Pipe size" 	 | 102666
		"screen_material"	 			  | "Plastic" 	 | 102666
		"screen_opening"	              | "Perforated Pipe" 	 | 102666
		"screen_bottom"	 				  | "Other" 	 | 107072
		"screen_from" 	 				  | "105" 	 | 105508
		"screen_to"	 					  | "109" 	 | 105508
		"internal_diameter"	 			  | "6" | 105508
		"assembly_type"	 				  | "Screen" 	 | 105508
		"slot_size"	 					  | "15" 	 | 105508
		"developed_by"	 				  | "Bailing" 	 | 110749
		"devlopment_total_duration"	 	  | "3 hours" 	 | 110749
		"yield_estimation_method"	      | "Air Lifting" 	 | 107072
		"yield_estimation_rate"			  | "15   USGPM" 	 | 110749
		"yield_estimation_duration"	 	  | "12   hours" 	 | 110749
		"casings_from"	 				  | "0" 	 | 113503
		"casings_to"	 				  | "63" 	 | 113503
		"casings_diameter"	 			  | "12.250" 	 | 112366
		"casings_material"	 			  | "Steel" 	 | 113503
		"casings_thickness"	 			  | "0.219" 	 | 113503
		"casings_driveshoe"	 			  | "Yes" 	 | 113503
		"surface_seal_method"	 		  | "Poured" 	 | 110627
		"surface_seal_material"	 		  | "Bentonite clay" 	 | 110627
		"surface_seal_thickness"	 	  | "2 inches" 	 | 105417
		"surface_seal_length"	 		  | "18 feet" 	 | 105417
		"backfill_type"	 				  | "CEMENT & BENTONITE CHIPS" 	 | 105417
		"backfill_depth"	 			  | "18 feet" 	 |  105417
		"liner_material"	 			  | "PVC" 	 |  111752
		"liner_diameter"	 			  | "4" 	 |  111752
		"liner_thickness"	 			  | "0.250" 	 |  111752
		"liner_from"	 				  | "8" 	 |  111752
		"liner_to"	 	  				  | "280" 	 |  111752
		"liner_perffrom"	 			  | "120" 	 |  111752
		"liner_perfto"	 				  | "140" 	 |  111752
		"lithology_from"	 			  | "0" 	 |  110000
        "lithology_to"	 				  | "2" 	 |  110000
        "lithology_raw_data"		      | "TOPSOIL, BROWN" 	 |  100001
        "lithology_description"	 		  | "cemented" 	 |  110000
        "lithology_material_description"  | "soil" 	 |  110000
        "lithology_relative_hardness"	  | "Stiff" 	 |  112152
        "lithology_colour" 	 			  | "dark" 	 |  110000
        "lithology_waterbearing_estimated_flow"	 | "200 USGPM" 	 |  104533
        "lithology_observations" 	 	  | "Water-bearing" 	 |  110000
        "reason_for_decommission" 	 	  | "SITE DEVELOPMENT" 	 |  110749
        "method_of_closure" 	 		  | "PUMPED" 	 |  110749
        "sealant_material" 	 			  | "CONCRETE" 	 |  110749
        "backfill_material" 	 		  | "BENTONITE AND GRAVEL" 	 |  100200
        "decommission_details"  	 	  | "NO ISSUES WITH CLOSURE. ONLY SLIGHT ARTESIAN FLOW IN NOV. 2014. CASING LEFT IN PLACE, PUMP PULLED." 	 |  110749
		"comments" 						  | "NOT RESPONSIBLE FOR QUALITY OR QUANTITY" | 110750
		"documentlink"					  | "WTN 109912_Well Construction.pdf" | 109912
		"no_document_msg"				  | "No additional documentation currently available for this well." | 100001
    }

/* 	@Issue("https://trello.com/c/mi3lnU5k")
	def "Find Aquifer Info"() {
		given: "I am a public user"
			go "gwells/well/102364"
		and: "that I want find out information about the aquifer my well is located in"
			at WellSummaryPage
			assert aquifer_number.text().trim() == "936"
			AquiferReport.aquiferNumber = "936"
		when: "I select the aquifer number from the Well Summary Page"
			withNewWindow ({ aquifer_number.click() }, page: AquiferReport, wait: true, close: false) {
		 		at AquiferReport
				}
		then: "a new window in my browser appears displaying the aquifer classification worksheet associated to that aquifer number."
			assert aquifer_number.text().trim() == "936"


	} */
}
