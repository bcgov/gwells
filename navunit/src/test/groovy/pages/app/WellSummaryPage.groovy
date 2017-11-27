package pages.app

import geb.Page

class WellSummaryPage extends Page {
    static at = { title == "Groundwater Wells Well Summary - Province of British Columbia" }
//    static url = "/well"

    static content = {
		summary_information { $( "fieldset", id:"summary_information") }
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
		screen_from { $("#screens > tbody > tr:nth-child(1) > td:nth-child(1)") }
        screen_to {  $("#screens > tbody > tr:nth-child(1) > td:nth-child(2)") }
        internal_diameter {  $("#screens > tbody > tr:nth-child(1) > td:nth-child(3)") }
        assembly_type {  $("#screens > tbody > tr:nth-child(1) > td:nth-child(4)") }
        slot_size {  $("#screens > tbody > tr:nth-child(1) > td:nth-child(5)") }

		developed_by { $( "span", id:"developed-by") }
		devlopment_total_duration { $( "span", id:"devlopment-total-duration") }

		yield_estimation_method { $( "span", id:"yield-estimation-method") }
		yield_estimation_rate { $( "span", id:"yield_estimation_rate") }
		yield_estimation_duration { $( "span", id:"yield_estimation_duration") }

		casing_field_set { $( "fieldset", id:"casing_field_set") }
		casings { $( "table", id:"casings") }
		casings_table { $("#casings td")*.text() }

		surface_seal_fieldset { $( "fieldset", id:"surface_seal_fieldset") }
		surface_seal_method { $( "span", id:"surface_seal_method") }
		surface_seal_material { $( "span", id:"surface_seal_material") }
		surface_seal_thickness { $( "span", id:"surface_seal_thickness") }
		surface_seal_length { $( "span", id:"surface_seal_length") }
		backfill_type { $( "span", id:"backfill_type") }
		backfill_depth { $( "span", id:"backfill_depth") }

		perforations_fieldset { $( "fieldset", id:"perforations_fieldset") }
		liner_details { $( "table", id:"liner_details") }
		liner_details_table { $("#liner_details td")*.text() }

		well_tag_number_link { $( "a", id:"well_tag_number_link") }
	}
}
