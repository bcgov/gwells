package pages.app

import geb.Page

class WellSummaryPage extends Page {
    static at = { title == "Groundwater Wells Well Summary - Province of British Columbia" }
//    static url = "/well"

    static content = {
			activitiesTable { $("table", id:"activities") }
			address { $("span", id:"address") }
			alternate_specs_submitted { $("span", id:"alternate_specs_submitted") }
			alteration_end_date { $("span", id:"alteration_end_date") }
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
			screensTable { $("table", id:"screens") }
			section { $("span", id:"section") }
			static_water_level { $("span", id:"static_water_level") }
			total_depth_drilled { $("span", id:"total_depth_drilled") }
			township { $("span", id:"township") }
			well_cap_type { $("span", id:"well_cap_type") }
			well_class { $("span", id:"well_class") }
			well_disinfected { $("span", id:"well_disinfected") }
			well_subclass { $("span", id:"well_subclass") }
			well_tag_number { $("span", id:"well_tag_number") }
			well_well_status { $("span", id:"well_well_status") }
			well_yield { $("span", id:"well_yield") }
			where_plate_attached { $("span", id:"where_plate_attached") }
			yieldsTable { $("table", id:"yields") }
    }
}
