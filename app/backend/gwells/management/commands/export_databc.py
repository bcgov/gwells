"""
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
import logging
import json
import os
import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import connection

from minio import Minio

from gwells.settings.base import get_env_variable
from gwells.management.commands import ResultIter

"""
Run from command line :
python manage.py export_databc

During development/testing it may be useful to instead run:
python manage.py export_databc --cleanup=0 --upload=0

This command runs in an OpenShift cronjob, defined in export.cj.json
"""

logger = logging.getLogger(__name__)

# IMPORTANT: If the underlying data structure changes (e.g. column name changes etc.), the
# property names have to stay the same! This endpoint is consumed by DataBC and must remain
# stable!
# Casing diameter: For now, grab the smallest diameter (should be using type, but we don't have
# date right now.)
# UPDATED FOR WATER-833, explicitly labelled column names (keeping older ones intact)
#   region was added to the export interface but is purposefully left empty, a new ticket will eventually
#   contain the added data
WELLS_SQL_V1 = ("""
select
    ST_AsGeoJSON(ST_Transform(geom, 4326)) :: json as "geometry",
    well.well_tag_number as well_tag_number,
    well.identification_plate_number as identification_plate_number,
    SUBSTRING(well_status_code.description for 255) as well_status,
    CASE WHEN licence_q.cur_licences > 0 THEN 'Licensed' ELSE 'Unlicensed' END as licence_status,
    SUBSTRING(CONCAT('https://apps.nrs.gov.bc.ca/gwells/well/', well.well_tag_number) for 255) as detail,
    well.artesian_flow as artesian_flow,
    SUBSTRING('usGPM' for 255) as artesian_flow_units,
    well.artesian_pressure as artesian_pressure,
    well.artesian_pressure_head as artesian_pressure_head,
    well.artesian_conditions as artesian_conditions,
    SUBSTRING(well_class_code.description for 100) as well_class,
    well_subclass_code.description as well_subclass,
    SUBSTRING(intended_water_use_code.description for 100) as intended_water_use,
    SUBSTRING(well.street_address for 100) as street_address,
    well.finished_well_depth as finished_well_depth,
    casing.diameter as diameter,
    well.static_water_level as static_water_level,
    well.bedrock_depth as bedrock_depth,
    well.well_yield as yield,
    SUBSTRING(well_yield_unit_code.description for 100) as yield_unit,
    well.aquifer_id as aquifer_id,
    well.observation_well_number as observation_well_number,
    well.obs_well_status_code as obs_well_status_code,
    well.well_identification_plate_attached as well_identification_plate_attached,
    well.water_supply_system_name as water_supply_system_name,
    well.water_supply_system_well_name as water_supply_system_well_name,
    well.city as city,
    well.legal_lot as legal_lot,
    well.legal_plan as legal_plan,
    well.legal_district_lot as legal_district_lot,
    well.legal_block as legal_block,
    well.legal_section as legal_section,
    well.legal_township as legal_township,
    well.legal_range as legal_range,
    well.land_district_code as land_district_code,
    well.legal_pid as legal_pid,
    well.well_location_description as well_location_description,
    ST_Y(ST_Transform(well.geom, 4326)) as latitude,
    ST_X(ST_Transform(well.geom, 4326)) as longitude,
    well.utm_zone_code as utm_zone_code,
    well.utm_northing as utm_northing,
    well.utm_easting as utm_easting,
    well.coordinate_acquisition_code as coordinate_acquisition_code,
    well.construction_start_date as construction_start_date,
    well.construction_end_date as construction_end_date,
    well.alteration_start_date as alteration_start_date,
    well.alteration_end_date as alteration_end_date,
    well.decommission_start_date as decommission_start_date,
    well.decommission_end_date as decommission_end_date,
    well.driller_name as driller_name,
    well.consultant_name as consultant_name,
    well.consultant_company as consultant_company,
    well.diameter as well_diameter,
    well.total_depth_drilled as total_depth_drilled,
    well.final_casing_stick_up as final_casing_stick_up,
    well.ground_elevation as ground_elevation,
    well.ground_elevation_method_code as ground_elevation_method_code,    
    well.well_yield as well_yield,
    well.well_yield_unit_code as well_yield_unit_code,
    well.well_cap_type as well_cap_type,
    well.well_disinfected_code as well_disinfected_code,
    well.well_orientation_code as well_orientation_code,
    well.alternative_specs_submitted as alternative_specs_submitted,
    well.surface_seal_material_code as surface_seal_material_code,
    well.surface_seal_method_code as surface_seal_method_code,
    null as surface_seal_length,
    well.surface_seal_depth as surface_seal_depth,
    well.surface_seal_thickness as surface_seal_thickness,
    well.backfill_type as backfill_type,
    well.backfill_depth as backfill_depth,
    well.liner_material_code as liner_material_code,
    well.liner_diameter as liner_diameter,
    well.liner_thickness as liner_thickness,
    well.liner_from as liner_from,
    well.liner_to as liner_to,
    well.screen_intake_method_code as screen_intake_method_code,
    well.screen_type_code as screen_type_code,
    well.screen_material_code as screen_material_code,
    well.other_screen_material as other_screen_material,
    well.screen_information as screen_information,
    well.screen_opening_code as screen_opening_code,
    well.screen_bottom_code as screen_bottom_code,
    well.other_screen_bottom as other_screen_bottom,
    well.filter_pack_from as filter_pack_from,
    well.filter_pack_to as filter_pack_to,
    well.filter_pack_material_code as filter_pack_material_code,
    well.filter_pack_thickness as filter_pack_thickness,
    well.filter_pack_material_size_code as filter_pack_material_size_code,
    well.development_hours as development_hours,
    well.development_notes as development_notes,
    well.water_quality_colour as water_quality_colour,
    well.water_quality_odour as water_quality_odour,
    (select string_agg(wwq.waterqualitycharacteristic_id::text, ',') 
        from well_water_quality wwq where wwq.well_id = well.well_tag_number) as water_quality_characteristics,
    well.yield_estimation_method_code as yield_estimation_method_code,
    well.yield_estimation_duration as yield_estimation_duration,
    well.drawdown as drawdown,
    well.hydro_fracturing_performed as hydro_fracturing_performed,
    well.hydro_fracturing_yield_increase as hydro_fracturing_yield_increase,
    well.decommission_reason as decommission_reason,
    well.decommission_method_code as decommission_method_code,
    well.decommission_details as decommission_details,
    well.decommission_sealant_material as decommission_sealant_material,
    well.decommission_backfill_material as decommission_backfill_material,
    well.comments as comments,
    well.ems as ems,
    SUBSTRING(CONCAT(registries_person.first_name, ' ', registries_person.surname) for 255) as person_responsible,
    registries_organization.name as company_of_person_responsible,
    well.aquifer_vulnerability_index as avi,
    well.storativity as storativity,
    well.transmissivity as transmissivity,
    well.hydraulic_conductivity as hydraulic_conductivity,
    well.specific_storage as specific_storage,
    well.specific_yield as specific_yield,
    well.testing_method as testing_method,
    well.testing_duration as testing_duration,
    well.analytic_solution_type as analytic_solution_type,
    well.boundary_effect_code as boundary_effect_code,
    well.aquifer_lithology_code as aquifer_lithology_code,
    well_licences.waterrightslicence_id as license_no,
    CASE WHEN well_licences.waterrightslicence_id IS NULL
        THEN NULL
        ELSE SUBSTRING(CONCAT('https://j200.gov.bc.ca/pub/ams/Default.aspx?PossePresentation=AMSPublic&PosseObjectDef=o_ATIS_DocumentSearch&PosseMenuName=WS_Main&Criteria_LicenceNumber=C',
            well_licences.waterrightslicence_id) for 512)
    END as licence_url,
    '' as region
from well
    left join well_status_code on well_status_code.well_status_code = well.well_status_code
    left join well_class_code on well_class_code.well_class_code = well.well_class_code
    left join well_subclass_code on well_subclass_code.well_subclass_guid = well.well_subclass_guid
    left join registries_person on registries_person.person_guid = well.person_responsible_guid
    left join registries_organization on registries_organization.org_guid = well.org_of_person_responsible_guid
    left join well_licences on well_licences.well_id = well.well_tag_number and well_licences.waterrightslicence_id = (
        select well_licences.waterrightslicence_id from well_licences
        where well_licences.well_id = well.well_tag_number
        and well_licences.waterrightslicence_id is not null
        order by well_licences.waterrightslicence_id desc limit 1)
    left join intended_water_use_code on
        intended_water_use_code.intended_water_use_code = well.intended_water_use_code
    left join well_yield_unit_code on
        well_yield_unit_code.well_yield_unit_code = well.well_yield_unit_code
    left join casing on
        casing.well_tag_number = well.well_tag_number and casing.casing_guid = (
            select casing.casing_guid from casing
            where casing.well_tag_number = well.well_tag_number
            order by casing.diameter asc limit 1)
    left join (select well_tag_number, count(*) as cur_licences from well
        join well_licences on
        well.well_tag_number = well_licences.well_id
        group by well_tag_number) as licence_q
        on well.well_tag_number = licence_q.well_tag_number
    where
        (well.well_publication_status_code = 'Published' or well.well_publication_status_code = null)
        and well.geom is not null
        {bounds}
    order by well.well_tag_number
""")

WELLS_SQL_V2 = ("""
select
    ST_AsGeoJSON(ST_Transform(geom, 4326)) :: json as "geometry",
    well.well_tag_number as well_tag_number,
    well.identification_plate_number as identification_plate_number,
    SUBSTRING(well_status_code.description for 255) as well_status,
    CASE WHEN licence_q.cur_licences > 0 THEN 'Licensed' ELSE 'Unlicensed' END as licence_status,
    SUBSTRING(CONCAT('https://apps.nrs.gov.bc.ca/gwells/well/', well.well_tag_number) for 255) as detail,
    well.artesian_flow as artesian_flow,
    SUBSTRING('usGPM' for 255) as artesian_flow_units,
    well.artesian_pressure as artesian_pressure,
    well.artesian_pressure_head as artesian_pressure_head,
    well.artesian_conditions as artesian_conditions,
    SUBSTRING(well_class_code.description for 100) as well_class,
    well_subclass_code.description as well_subclass,
    SUBSTRING(intended_water_use_code.description for 100) as intended_water_use,
    SUBSTRING(well.street_address for 100) as street_address,
    well.finished_well_depth as finished_well_depth,
    casing.diameter as diameter,
    well.static_water_level as static_water_level,
    well.bedrock_depth as bedrock_depth,
    well.well_yield as yield,
    SUBSTRING(well_yield_unit_code.description for 100) as yield_unit,
    well.aquifer_id as aquifer_id,
    well.observation_well_number as observation_well_number,
    well.obs_well_status_code as obs_well_status_code,
    well.well_identification_plate_attached as well_identification_plate_attached,
    well.water_supply_system_name as water_supply_system_name,
    well.water_supply_system_well_name as water_supply_system_well_name,
    well.city as city,
    well.legal_lot as legal_lot,
    well.legal_plan as legal_plan,
    well.legal_district_lot as legal_district_lot,
    well.legal_block as legal_block,
    well.legal_section as legal_section,
    well.legal_township as legal_township,
    well.legal_range as legal_range,
    well.land_district_code as land_district_code,
    well.legal_pid as legal_pid,
    well.well_location_description as well_location_description,
    ST_Y(ST_Transform(well.geom, 4326)) as latitude,
    ST_X(ST_Transform(well.geom, 4326)) as longitude,
    well.utm_zone_code as utm_zone_code,
    well.utm_northing as utm_northing,
    well.utm_easting as utm_easting,
    well.coordinate_acquisition_code as coordinate_acquisition_code,
    well.construction_start_date as construction_start_date,
    well.construction_end_date as construction_end_date,
    well.alteration_start_date as alteration_start_date,
    well.alteration_end_date as alteration_end_date,
    well.decommission_start_date as decommission_start_date,
    well.decommission_end_date as decommission_end_date,
    well.driller_name as driller_name,
    well.consultant_name as consultant_name,
    well.consultant_company as consultant_company,
    well.diameter as well_diameter,
    well.total_depth_drilled as total_depth_drilled,
    well.final_casing_stick_up as final_casing_stick_up,
    well.ground_elevation as ground_elevation,
    well.ground_elevation_method_code as ground_elevation_method_code,    
    well.well_yield as well_yield,
    well.well_yield_unit_code as well_yield_unit_code,
    well.well_cap_type as well_cap_type,
    well.well_disinfected_code as well_disinfected_code,
    well.well_orientation_code as well_orientation_code,
    well.alternative_specs_submitted as alternative_specs_submitted,
    well.surface_seal_material_code as surface_seal_material_code,
    well.surface_seal_method_code as surface_seal_method_code,    
    well.surface_seal_depth as surface_seal_depth,
    well.surface_seal_thickness as surface_seal_thickness,
    well.backfill_type as backfill_type,
    well.backfill_depth as backfill_depth,
    well.liner_material_code as liner_material_code,
    well.liner_diameter as liner_diameter,
    well.liner_thickness as liner_thickness,
    well.liner_from as liner_from,
    well.liner_to as liner_to,
    well.screen_intake_method_code as screen_intake_method_code,
    well.screen_type_code as screen_type_code,
    well.screen_material_code as screen_material_code,
    well.other_screen_material as other_screen_material,
    well.screen_information as screen_information,
    well.screen_opening_code as screen_opening_code,
    well.screen_bottom_code as screen_bottom_code,
    well.other_screen_bottom as other_screen_bottom,
    well.filter_pack_from as filter_pack_from,
    well.filter_pack_to as filter_pack_to,
    well.filter_pack_material_code as filter_pack_material_code,
    well.filter_pack_thickness as filter_pack_thickness,
    well.filter_pack_material_size_code as filter_pack_material_size_code,
    well.development_hours as development_hours,
    well.development_notes as development_notes,
    well.water_quality_colour as water_quality_colour,
    well.water_quality_odour as water_quality_odour,
    (select string_agg(wwq.waterqualitycharacteristic_id::text, ',') 
        from well_water_quality wwq where wwq.well_id = well.well_tag_number) as water_quality_characteristics,
    well.yield_estimation_method_code as yield_estimation_method_code,
    well.yield_estimation_duration as yield_estimation_duration,
    well.drawdown as drawdown,
    well.hydro_fracturing_performed as hydro_fracturing_performed,
    well.hydro_fracturing_yield_increase as hydro_fracturing_yield_increase,
    well.decommission_reason as decommission_reason,
    well.decommission_method_code as decommission_method_code,
    well.decommission_details as decommission_details,
    well.decommission_sealant_material as decommission_sealant_material,
    well.decommission_backfill_material as decommission_backfill_material,
    well.comments as comments,
    well.ems as ems,
    SUBSTRING(CONCAT(registries_person.first_name, ' ', registries_person.surname) for 255) as person_responsible,
    registries_organization.name as company_of_person_responsible,
    well.aquifer_vulnerability_index as avi,
    well.storativity as storativity,
    well.transmissivity as transmissivity,
    well.hydraulic_conductivity as hydraulic_conductivity,
    well.specific_storage as specific_storage,
    well.specific_yield as specific_yield,
    well.testing_method as testing_method,
    well.testing_duration as testing_duration,
    well.analytic_solution_type as analytic_solution_type,
    well.boundary_effect_code as boundary_effect_code,
    well.aquifer_lithology_code as aquifer_lithology_code,
    well_licences.waterrightslicence_id as license_no,
    CASE WHEN well_licences.waterrightslicence_id IS NULL
        THEN NULL
        ELSE SUBSTRING(CONCAT('https://j200.gov.bc.ca/pub/ams/Default.aspx?PossePresentation=AMSPublic&PosseObjectDef=o_ATIS_DocumentSearch&PosseMenuName=WS_Main&Criteria_LicenceNumber=C',
            well_licences.waterrightslicence_id) for 512)
    END as licence_url,
    '' as region
from well
    left join well_status_code on well_status_code.well_status_code = well.well_status_code
    left join well_class_code on well_class_code.well_class_code = well.well_class_code
    left join well_subclass_code on well_subclass_code.well_subclass_guid = well.well_subclass_guid
    left join registries_person on registries_person.person_guid = well.person_responsible_guid
    left join registries_organization on registries_organization.org_guid = well.org_of_person_responsible_guid
    left join well_licences on well_licences.well_id = well.well_tag_number and well_licences.waterrightslicence_id = (
        select well_licences.waterrightslicence_id from well_licences
        where well_licences.well_id = well.well_tag_number
        and well_licences.waterrightslicence_id is not null
        order by well_licences.waterrightslicence_id desc limit 1)
    left join intended_water_use_code on
        intended_water_use_code.intended_water_use_code = well.intended_water_use_code
    left join well_yield_unit_code on
        well_yield_unit_code.well_yield_unit_code = well.well_yield_unit_code
    left join casing on
        casing.well_tag_number = well.well_tag_number and casing.casing_guid = (
            select casing.casing_guid from casing
            where casing.well_tag_number = well.well_tag_number
            order by casing.diameter asc limit 1)
    left join (select well_tag_number, count(*) as cur_licences from well
        join well_licences on
        well.well_tag_number = well_licences.well_id
        group by well_tag_number) as licence_q
        on well.well_tag_number = licence_q.well_tag_number
    where
        (well.well_publication_status_code = 'Published' or well.well_publication_status_code = null)
        and well.geom is not null
        {bounds}
    order by well.well_tag_number
""")
WELL_CHUNK_SIZE = 10000

# IMPORTANT: If the underlying data structure changes (e.g. column name changes etc.), the
# property names have to stay the same! This endpoint is consumed by DataBC and must remain
# stable!
LITHOLOGY_SQL = ("""
select
    ST_AsGeoJSON(ST_Transform(geom, 4326)) :: json as "geometry",
    well.well_tag_number,
    identification_plate_number,
    SUBSTRING(well_status_code.description for 255) as well_status,
    CASE WHEN licence_q.cur_licences > 0 THEN 'Licensed' ELSE 'Unlicensed' END as licence_status,
    SUBSTRING(CONCAT('https://apps.nrs.gov.bc.ca/gwells/well/', well.well_tag_number) for 255) as detail,
    lithology_description.lithology_from as from,
    lithology_description.lithology_to as to,
    SUBSTRING(lithology_colour_code.description for 100) as colour,
    SUBSTRING(lithology_description_code.description for 255) as description,
    SUBSTRING(lithology_material_code.description for 255) as material,
    SUBSTRING(lithology_description.lithology_observation for 250) as observation,
    SUBSTRING(lithology_hardness_code.description for 100) as hardness,
    SUBSTRING(well_class_code.description for 100) as well_class,
    SUBSTRING(intended_water_use_code.description for 100) as intended_water_use,
    SUBSTRING(well.street_address for 100) as street_address,
    well.finished_well_depth,
    casing.diameter,
    well.static_water_level,
    well.bedrock_depth,
    well.well_yield as yield,
    SUBSTRING(well_yield_unit_code.description for 100) as yield_unit,
    well.aquifer_id as aquifer_id,
    lithology_description.lithology_raw_data as raw_data
from well
    inner join lithology_description on
        lithology_description.well_tag_number = well.well_tag_number
    left join well_status_code on
        well_status_code.well_status_code = well.well_status_code
    left join lithology_material_code on
        lithology_material_code.lithology_material_code =
            lithology_description.lithology_material_code
    left join lithology_colour_code on
        lithology_colour_code.lithology_colour_code = lithology_description.lithology_colour_code
    left join lithology_description_code on
        lithology_description_code.lithology_description_code =
            lithology_description.lithology_description_code
    left join lithology_hardness_code on
        lithology_hardness_code.lithology_hardness_code =
            lithology_description.lithology_hardness_code
    left join well_class_code on well_class_code.well_class_code = well.well_class_code
    left join intended_water_use_code on
        intended_water_use_code.intended_water_use_code = well.intended_water_use_code
    left join well_yield_unit_code on
        well_yield_unit_code.well_yield_unit_code = well.well_yield_unit_code
    left join casing on
        casing.well_tag_number = well.well_tag_number and casing.casing_guid = (
            select casing.casing_guid from casing
            where casing.well_tag_number = well.well_tag_number
            order by casing.diameter asc limit 1)
    left join (select well_tag_number, count(*) as cur_licences from well
        join well_licences on
        well.well_tag_number = well_licences.well_id
        group by well_tag_number) as licence_q
        on well.well_tag_number = licence_q.well_tag_number
    where
        (well.well_publication_status_code = 'Published' or well.well_publication_status_code = null)
        and well.geom is not null
        {bounds}
    order by well.well_tag_number, lithology_description.lithology_from
""")
LITHOLOGY_CHUNK_SIZE = 10000

# IMPORTANT: If the underlying data structure changes (e.g. column name changes etc.), the
# property names have to stay the same! This endpoint is consumed by DataBC and must remain
# stable!
AQUIFERS_SQL_V1 = ("""
select
    ST_AsGeoJSON(ST_Transform(ST_GeometryN(geom, 1), 4326)) :: json as "geometry",
    aquifer.aquifer_id as aquifer_id,
    SUBSTRING(aquifer.aquifer_name for 100) as name,
    SUBSTRING(aquifer.location_description for 100) as location,
    SUBSTRING(CONCAT('https://apps.nrs.gov.bc.ca/gwells/aquifers/', aquifer.aquifer_id) for 255) as detail,
    SUBSTRING(
        CASE WHEN aquifer_material_code.aquifer_material_code IN ('G', 'S', 'GS') THEN
            'Sand and Gravel'
        ELSE
            aquifer_material_code.description
        END
    for 100) AS material,
    SUBSTRING(aquifer_subtype_code.description for 100) as subtype,
    SUBSTRING(aquifer_vulnerability_code.description for 100) as vulnerability,
    SUBSTRING(aquifer_productivity_code.description for 100) as productivity,
    SUBSTRING(aquifer_demand_code.description for 100) as demand,
    SUBSTRING(water_use_code.description for 100) as water_use,
    SUBSTRING(quality_concern_code.description for 100) as quality_concern,
    SUBSTRING(aquifer.litho_stratographic_unit for 100) as litho_stratographic_unit,
    aquifer.mapping_year,
    SUBSTRING(aquifer.notes for 2000) as notes
from aquifer
    left join aquifer_material_code on
        aquifer_material_code.aquifer_material_code = aquifer.aquifer_material_code
    left join aquifer_subtype_code on
        aquifer_subtype_code.aquifer_subtype_code = aquifer.aquifer_subtype_code
    left join aquifer_vulnerability_code on
        aquifer_vulnerability_code.aquifer_vulnerability_code = aquifer.aquifer_vulnerablity_code
    left join aquifer_productivity_code on
        aquifer_productivity_code.aquifer_productivity_code = aquifer.aquifer_productivity_code
    left join aquifer_demand_code on
        aquifer_demand_code.aquifer_demand_code = aquifer.aquifer_demand_code
    left join water_use_code on
        water_use_code.water_use_code = aquifer.water_use_code
    left join quality_concern_code on
        quality_concern_code.quality_concern_code = aquifer.quality_concern_code
    where
        aquifer.geom is not null AND
        aquifer.effective_date <= NOW() AND aquifer.expiry_date >= NOW() AND
        aquifer.retire_date >= NOW()
        {bounds}
    order by aquifer.aquifer_id
""")

AQUIFERS_SQL_V2 = ("""
SELECT
    ST_AsGeoJSON(ST_Transform(a.geom, 4326)) :: json AS "geometry",
    a.aquifer_id AS aquifer_id,
    SUBSTRING(a.aquifer_name for 100) AS name,
    SUBSTRING(a.location_description for 100) AS location,
    SUBSTRING(CONCAT('https://apps.nrs.gov.bc.ca/gwells/aquifers/', a.aquifer_id) for 255) AS detail,
    SUBSTRING(
        CASE WHEN aquifer_material_code.aquifer_material_code IN ('G', 'S', 'GS') THEN
            'Sand and Gravel'
        ELSE
            aquifer_material_code.description
        END
    for 100) AS material,
    SUBSTRING(aquifer_subtype_code.description for 100) AS subtype,
    SUBSTRING(aquifer_vulnerability_code.description for 100) AS vulnerability,
    SUBSTRING(aquifer_productivity_code.description for 100) AS productivity,
    SUBSTRING(aquifer_demand_code.description for 100) AS demand,
    SUBSTRING(water_use_code.description for 100) AS water_use,
    SUBSTRING(quality_concern_code.description for 100) AS quality_concern,
    SUBSTRING(a.litho_stratographic_unit for 100) AS litho_stratographic_unit,
    a.mapping_year,
    a.retire_date,
    SUBSTRING(a.notes for 2000) AS notes
FROM aquifer AS a
    LEFT JOIN aquifer_material_code on
        aquifer_material_code.aquifer_material_code = a.aquifer_material_code
    LEFT JOIN aquifer_subtype_code on
        aquifer_subtype_code.aquifer_subtype_code = a.aquifer_subtype_code
    LEFT JOIN aquifer_vulnerability_code on
        aquifer_vulnerability_code.aquifer_vulnerability_code = a.aquifer_vulnerablity_code
    LEFT JOIN aquifer_productivity_code on
        aquifer_productivity_code.aquifer_productivity_code = a.aquifer_productivity_code
    LEFT JOIN aquifer_demand_code on
        aquifer_demand_code.aquifer_demand_code = a.aquifer_demand_code
    LEFT JOIN water_use_code on
        water_use_code.water_use_code = a.water_use_code
    LEFT JOIN quality_concern_code on
        quality_concern_code.quality_concern_code = a.quality_concern_code
    WHERE
        a.geom is not null AND
        a.effective_date <= NOW() AND a.expiry_date >= NOW() AND
        a.retire_date >= NOW()
        {bounds}
    ORDER BY a.aquifer_id
""")
AQUIFER_CHUNK_SIZE = 100


class LazyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


class GeoJSONIterator():

    def __init__(self, sql, chunk_size, cursor, bounds=None):
        self.send_header = True
        self.done = False
        self.first_record = True
        params = ()
        if bounds:
            params = bounds
        cursor.execute(sql, params)
        self.iterator = ResultIter(cursor, chunk_size)
        self.fields = self.get_fields(cursor)

    def get_header(self):
        return """{"type": "FeatureCollection","features": ["""

    def get_footer(self):
        return ']}'

    def format_record(self, record):
        """ Write a single record to file."""
        feature = {
            'type': 'Feature',
            'geometry': record[0],
            'properties': {}
        }
        for col, value in enumerate(record):
            if self.fields[col] != 'geometry':
                feature['properties'][self.fields[col]] = value
        return json.dumps(feature, cls=LazyEncoder)

    def get_fields(self, cursor):
        fields = []
        for index, field in enumerate(cursor.description):
            field_name = field[0]
            fields.append(field_name)
        return fields

    def __iter__(self):
        return self

    def __next__(self):
        if self.send_header:
            # If we're right at the start, send the header.
            self.send_header = False
            return self.get_header()
        elif self.done:
            # If we're done, be done!
            raise StopIteration
        else:
            # If we're chugging along, send a record.
            try:
                record = next(self.iterator)
                record = self.format_record(record)
                if self.first_record:
                    self.first_record = False
                else:
                    record = ',{}'.format(record)
                return '\n{}'.format(record)
            except StopIteration:
                # No more records? Send the footer.
                self.done = True
                return self.get_footer()


class Command(BaseCommand):

    def __init__(self):
        """
        declare our class variables
        versions and output file names
        """
        super().__init__()
        self.version1 = 'v1'
        self.version2 = 'v2'
        self.versions = [self.version1, self.version2]
        self.wells_filename = 'wells.json'
        self.aquifers_filename = 'aquifers.json'
        self.lithology_filename = 'lithology.json'

    def add_arguments(self, parser):
        # Arguments added for debugging purposes.
        # e.g. don't cleanup, don't upload: python manage.py export_databc --cleanup=0 --upload=0
        parser.add_argument('--cleanup', type=int, nargs='?', help='If 1, remove file when done', default=1)
        parser.add_argument('--upload', type=int, nargs='?', help='If 1, upload the file', default=1)

    def handle(self, *args, **options):
        """
        Entry point for Django Command.
        for each version (v1, v2), generate our outputs,
            upload our files if option is set,
            cleanup our filesystem if option is set
        """
        files = (self.wells_filename, self.aquifers_filename, self.lithology_filename)

        for version in self.versions:
            self.generate_by_version(version)
            if options['upload'] == 1:
                self.upload_files(files, version)

        if options['cleanup'] == 1:
            self.cleanup(files)

        logger.info('GeoJSON export complete.')
        self.stdout.write(self.style.SUCCESS('GeoJSON export complete.'))

    def generate_by_version(self, version):
        """
        generate outputs for each version.
        wells and lithology are the same outputs for both version1 and version2
        aquifer outputs differ between versions so always output
        :param version: the version number of the file to generate data for
        """
        logger.info(f'Starting GeoJSON {version} export.')
        if version == self.version1:
            self.generate_lithology(self.lithology_filename)
        self.generate_wells(self.wells_filename, version)
        self.generate_aquifers(self.aquifers_filename, version)

    def cleanup(self, files):
        """Delete all local files GeoJSON files."""
        for filename in files:
            if os.path.exists(filename):
                os.remove(filename)

    def upload_files(self, files, version):
        """Upload files to S3 bucket."""
        is_secure = get_env_variable('S3_USE_SECURE', '1', warn=False) is '1'
        minio_client = Minio(get_env_variable('S3_HOST'),
                             access_key=get_env_variable('S3_PUBLIC_ACCESS_KEY'),
                             secret_key=get_env_variable('S3_PUBLIC_SECRET_KEY'),
                             secure=is_secure)
        for filename in files:
            logger.info('uploading {}'.format(filename))
            with open(filename, 'rb') as file_data:
                file_stat = os.stat(filename)
                target = f'api/{version}/gis/{filename}'
                bucket = get_env_variable('S3_WELL_EXPORT_BUCKET')
                logger.debug(
                    'uploading {} to {}/{}'.format(filename, bucket, target))
                minio_client.put_object(bucket,
                                        target,
                                        file_data,
                                        file_stat.st_size)

    def generate_geojson_chunks(self, sql, target, chunk_size):
        logger.info('Generating GeoJSON for {}'.format(target))
        # Open JSON file to write to.
        with connection.cursor() as cursor:
            with open(target, 'w') as f:
                reader = GeoJSONIterator(sql, chunk_size, cursor)
                count = 0
                for item in reader:
                    f.write('{}\n'.format(item))
                    count += 1

    def generate_lithology(self, filename):
        self.generate_geojson_chunks(LITHOLOGY_SQL.format(bounds=''),
                                     filename,
                                     LITHOLOGY_CHUNK_SIZE)

    def generate_aquifers(self, filename, version):
        """
        based on version, use the applicable sql statement version to
            generate our geojson chunks in a file
        :param filename: the filename to generate our geojson chunk into
        :param version: the version number of the sql statement to use
        """
        if version == self.version2:
            self.generate_geojson_chunks(AQUIFERS_SQL_V2.format(bounds=''),
                                         filename,
                                         AQUIFER_CHUNK_SIZE)
        else:
            self.generate_geojson_chunks(AQUIFERS_SQL_V1.format(bounds=''),
                                         filename,
                                         AQUIFER_CHUNK_SIZE)

    def generate_wells(self, filename, version):
        """
        based on version, use the applicable sql statement version to
            generate our geojson chunks in a file
        :param filename: the filename to generate our geojson chunk into
        :param version: the version number of the sql statement to use
        """
        if version == self.version2:
            self.generate_geojson_chunks(WELLS_SQL_V2.format(bounds=''),
                                         filename,
                                         AQUIFER_CHUNK_SIZE)
        else:
            self.generate_geojson_chunks(WELLS_SQL_V1.format(bounds=''),
                                         filename,
                                         WELL_CHUNK_SIZE)
