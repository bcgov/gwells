package pages.app

import geb.Page

class WellSummaryPage extends Page {
    static at = { title == "Groundwater Wells Well Summary - Province of British Columbia" }
//    static url = "/well"

    static content = {
		summary_information { $( "fieldset", id:"summary_information_fieldset") }
		well_tag_number { $( "span", id:"well_tag_number") }
		identification_plate_number { $( "span", id:"identification_plate_number") }
		owner_full_name { $( "span", id:"owner_full_name") }
		licenced_status { $( "span", id:"licenced_status") }
		well_well_status { $( "span", id:"well_well_status") }
		well_class { $( "span", id:"well_class") }
		well_subclass { $( "span", id:"well_subclass") }
		intended_water_use { $( "span", id:"intended_water_use") }
		obs_well_number { $( "span", id:"obs_well_number") }
		obs_well_status { $( "span", id:"obs_well_status") }
		ems_id { $( "span", id:"ems_id") }
		aquifer_number { $( "span", id:"aquifer_number") }
		alternate_specs_submitted { $( "span", id:"alternate_specs_submitted") }
		water_supply_system_name { $( "span", id:"water_supply_system_name") }
		water_supply_system_well_name { $( "span", id:"water_supply_system_well_name") }

		address { $( "span", id:"address") }
		city { $( "span", id:"city") }
		legal { $( "table", id:"legal") }
		lot { $( "span", id:"lot") }
		plan { $( "span", id:"plan") }
		district_lot { $( "span", id:"district_lot") }
		block { $( "span", id:"block") }
		section { $( "span", id:"section") }
		township { $( "span", id:"township") }
		range { $( "span", id:"range") }
		land_district { $( "span", id:"land_district") }
		pid { $( "span", id:"pid") }

		location_desc { $( "span", id:"location_desc") }
		latitude { $( "span", id:"latitude") }
		longitude { $( "span", id:"longitude") }
		utm_zone_code { $( "span", id:"utm_zone_code") }
		utm_northing { $( "span", id:"utm_northing") }
		utm_easting { $( "span", id:"utm_easting") }
		utm_accuracy_code { $( "span", id:"utm_accuracy_code") }
		bcgs_mapsheet_number { $( "span", id:"bcgs_mapsheet_number") }

		activities { $( "table", id:"activities") }
		activities_table { $("#activities td")*.text() }
		construction_end_date { $("#activities td",0) }
		alteration_end_date { $("#activities td",1) }
		decommission_end_date { $("#activities td",2) }
		drilling_company { $("#activities td",3) }

		total_depth_drilled { $( "span", id:"total_depth_drilled") }
		static_water_level { $( "span", id:"static_water_level") }
		well_cap_type { $( "span", id:"well_cap_type") }
		finished_well_depth { $( "span", id:"finished_well_depth") }
		well_yield { $( "span", id:"well_yield") }
		well_disinfected { $( "span", id:"well_disinfected") }
		final_casing_stickup { $( "span", id:"final_casing_stickup") }
		artesian_flow { $( "span", id:"artesian_flow") }
		drilling_method { $( "span", id:"drilling_method") }
		bedrock_depth { $( "span", id:"bedrock_depth") }
		artesian_pressure { $( "span", id:"artesian_pressure") }
		orientation_direction { $( "span", id:"orientation2") }
		ground_elevation { $( "span", id:"ground_elevation") }
		ground_elevation_method { $( "span", id:"ground_elevation_method") }
		well_plate_attached { $( "span", id:"well_plate_attached") }

		intake_method { $( "span", id:"intake_method") }
		screen_type { $( "span", id:"screen_type") }
		screen_material { $( "span", id:"screen_material") }
		screen_opening { $( "span", id:"screen_opening") }
		screen_bottom { $( "span", id:"screen_bottom") }
		screens { $( "table", id:"screens") }
		screens_table { $( "#screens td")*.text() }

    no_screen_information { $( "span", id:"no_screen_information" ) }

		screen_from { $("#screens > tbody > tr:nth-child(2) > td:nth-child(1)") }
        screen_to {  $("#screens > tbody > tr:nth-child(2) > td:nth-child(2)") }
        internal_diameter {  $("#screens > tbody > tr:nth-child(2) > td:nth-child(3)") }
        assembly_type {  $("#screens > tbody > tr:nth-child(2) > td:nth-child(4)") }
        slot_size {  $("#screens > tbody > tr:nth-child(2) > td:nth-child(5)") }

		developed_by { $( "span", id:"developed-by") }
		devlopment_total_duration { $( "span", id:"devlopment-total-duration") }

		yield_estimation_method { $( "span", id:"yield-estimation-method") }
		yield_estimation_rate { $( "span", id:"yield_estimation_rate") }
		yield_estimation_duration { $( "span", id:"yield_estimation_duration") }

		casing_field_set { $( "fieldset", id:"casing_fieldset") }
		casings { $( "table", id:"casings") }
		casings_table { $("#casings td")*.text() }
    no_casing_information { $( "span", id:"no_casing_information" ) }
		casings_from { $("#casings > tbody > tr:nth-child(1) > td:nth-child(1)") }
		casings_to { $("#casings > tbody > tr:nth-child(1) > td:nth-child(2)") }
		casings_diameter { $("#casings > tbody > tr:nth-child(1) > td:nth-child(3)") }
		casings_material { $("#casings > tbody > tr:nth-child(1) > td:nth-child(4)") }
		casings_thickness { $("#casings > tbody > tr:nth-child(1) > td:nth-child(5)") }
		casings_driveshoe { $("#casings > tbody > tr:nth-child(1) > td:nth-child(6)") }

		surface_seal_fieldset { $( "fieldset", id:"surface_seal_fieldset") }
		surface_seal_method { $( "span", id:"surface_seal_method") }
		surface_seal_material { $( "span", id:"surface_seal_material") }
		surface_seal_thickness { $( "span", id:"surface_seal_thickness") }
		surface_seal_length { $( "span", id:"surface_seal_length") }
		backfill_type { $( "span", id:"backfill_type") }
		backfill_depth { $( "span", id:"backfill_depth") }

		perforations_fieldset { $( "fieldset", id:"perforations_fieldset") }
		liner_details { $( "table", id:"liner_details") }
    no_liner_details_information { $("span", id:"no_liner_details_information") }

		liner_details_table { $("#liner_details td")*.text() }
		liner_material { $("#liner_details > tbody > tr:nth-child(1) > td:nth-child(1)") }
		liner_diameter { $("#liner_details > tbody > tr:nth-child(1) > td:nth-child(2)") }
		liner_thickness { $("#liner_details > tbody > tr:nth-child(1) > td:nth-child(3)") }
		liner_from { $("#liner_details > tbody > tr:nth-child(1) > td:nth-child(4)") }
		liner_to { $("#liner_details > tbody > tr:nth-child(1) > td:nth-child(5)") }
		liner_perffrom  { $("#liner_details > tbody > tr:nth-child(1) > td:nth-child(6)") }
		liner_perfto { $("#liner_details > tbody > tr:nth-child(1) > td:nth-child(7)") }

		lithology_fieldset { $( "fieldset", id:"lithology_fieldset") }
		lithology { $( "table", id:"lithology") }
    no_lithology_information { $( "span", id:"no_lithology_information" ) }
		lithology_table { $("#lithology td")*.text() }

		lithology_from { $("#lithology > tbody > tr:nth-child(1) > td:nth-child(1)") }
        lithology_to { $("#lithology > tbody > tr:nth-child(1) > td:nth-child(2)") }
        lithology_raw_data { $("#lithology > tbody > tr:nth-child(1) > td:nth-child(3)") }
        lithology_description { $("#lithology > tbody > tr:nth-child(6) > td:nth-child(4)") }
        lithology_material_description { $("#lithology > tbody > tr:nth-child(1) > td:nth-child(5)") }
        lithology_relative_hardness { $("#lithology > tbody > tr:nth-child(1) > td:nth-child(6)") }
        lithology_colour { $("#lithology > tbody > tr:nth-child(1) > td:nth-child(7)") }
        lithology_waterbearing_estimated_flow { $("#lithology > tbody > tr:nth-child(3) > td:nth-child(8)") }
        lithology_observations { $("#lithology > tbody > tr:nth-child(7) > td:nth-child(9)") }

		well_decommissioning { $( "fieldset", id:"well_decommissioning_fieldset") }
        reason_for_decommission { $( "span", id:"reason_for_decommission") }
        method_of_closure { $( "span", id:"method_of_closure") }
        sealant_material { $( "span", id:"sealant_material") }
        backfill_material { $( "span", id:"backfill_material") }
        decommission_details { $( "span", id:"decommission_details") }

		comments { $("span", id:"comments") }

		no_document_msg { $("#no_documentation_msg") }
		documentlink { $("#additional_documentation_table > tbody > tr > td > a") }

	}
}
