package pages.app

import geb.Page

class WellSummaryPage extends Page {
    static at = { title == "Groundwater Wells Well Summary - Province of British Columbia" }
//    static url = "/well"

    static content = {
			activitiesTable { $("table", id:"activities") }
			address { $("span", id:"address") }
			alteration_end_date { $("span", id:"alteration_end_date") }
			alternate_specs_submitted { $("span", id:"alternate_specs_submitted") }
			aquifer_number { $("span", id:"aquifer_number") }
			backfill_depth { $("span", id:"backfill_depth") }
			backfill_type { $("span", id:"backfill_type") }
			block { $("span", id:"block") }
			casingsTable { $("table", id:"casings") }
			city { $("span", id:"city") }
			construction_end_date { $("span", id:"construction_end_date") } 
			decommission_end_date { $("span", id:"decommission_end_date") }
			district_lot { $("span", id:"district_lot") }
			drilling_company { $("span", id:"drilling_company") }
			ems_id { $("span", id:"ems_id") }
			finished_well_depth { $("span", id:"finished_well_depth") }
			identification_plate_number { $("span", id:"identification_plate_number") }
			intended_water_use { $("span", id:"intended_water_use") }
			land_district { $("span", id:"land_district") }
			latitude { $("span", id:"latitude") }
			legalTable { $("table", id:"legal") }
			licenced_status { $("span", id:"licenced_status") }
			location_desc { $("span", id:"location_desc") }
			longitude { $("span", id:"longitude") }
			lot { $("span", id:"lot") }
			obs_well_number { $("span", id:"obs_well_number") }
			obs_well_status { $("span", id:"obs_well_status") }
			owner_full_name { $("span", id:"owner_full_name") }
			pid { $("span", id:"pid") }
			plan { $("span", id:"plan") }
			range { $("span", id:"range") }
			screen_bottom { $("span", id:"screen_bottom") }
			screen_material { $("span", id:"screen_material") }
			screen_opening { $("span", id:"screen_opening") }
			screen_type { $("span", id:"screen_type") }
			screensTable { $("table", id:"screens") }
			section { $("span", id:"section") }
			static_water_level { $("span", id:"static_water_level") }
			surface_seal_material { $("span", id:"screen_type") }
			surface_seal_thickness { $("span", id:"screen_type") }
			total_depth_drilled { $("span", id:"total_depth_drilled") }
			township { $("span", id:"township") }
			water_supply_system_name { $("span", id:"water_supply_system_name") }
			water_supply_system_well_name { $("span", id:"water_supply_system_well_name") }
			well_cap_type { $("span", id:"well_cap_type") }
			well_class { $("span", id:"well_class") }
			well_disinfected { $("span", id:"well_disinfected") }
			well_plate_attached { $("span", id:"well_plate_attached") }
			well_subclass { $("span", id:"well_subclass") }
			well_tag_number { $("span", id:"well_tag_number") }
			well_well_status { $("span", id:"well_well_status") }
			well_yield { $("span", id:"well_yield") }
			yield_estimation_duration { $("span", id:"yield_estimation_duration") }
			yield_estimation_method { $("span", id:"yield-estimation-method") }
			yield_estimation_rate { $("span", id:"yield_estimation_rate") }
	}
}
