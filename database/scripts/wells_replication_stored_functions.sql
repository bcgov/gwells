/*
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/
--
--  PostgreSQL script to create stored functions that replicate legacy
--  WELLS data from production Oracle Database, to the GWELLS application
--  database.
--
--  These stored functions will not be needed once we cut over
--  from legacy WELLS to the new GWELLS application.
--

-- DESCRIPTION
--   Define the SQL INSERT command that copies from the legacy WELLS table to a temporary
--   ETL or 'transformation' (i.e. *_xform) table using dynamic SQL to support the optional
--   SQL subset clause.
--
-- PARAMETERS
--   _subset_ind Boolean indicator flag: 'true' to append additional WHERE clause, limiting
--                                       the copy to a smaller subset
--                                       'false' to copy ALL data
-- RETURNS
--   None as this is a stored procedure
--
CREATE OR REPLACE FUNCTION populate_xform(
  _subset_ind boolean DEFAULT true) RETURNS void AS $$
DECLARE
  xform_rows integer;
  sql_stmt text;
  subset_clause text := 'AND wells.well_tag_number between 100001 and 113567';
  insert_sql    text := 'INSERT INTO xform_well (
    well_tag_number                ,
    well_id                        ,
    well_guid                      ,
    acceptance_status_code         ,
    owner_full_name                ,
    owner_mailing_address          ,
    owner_city                     ,
    owner_postal_code              ,
    street_address                 ,
    city                           ,
    legal_lot                      ,
    legal_plan                     ,
    legal_district_lot             ,
    legal_block                    ,
    legal_section                  ,
    legal_township                 ,
    legal_range                    ,
    legal_pid                      ,
    well_location_description      ,
    identification_plate_number    ,
    diameter                       ,
    total_depth_drilled            ,
    finished_well_depth            ,
    static_water_level             ,
    well_cap_type                  ,
    well_disinfected               ,
    well_yield                     ,
    intended_water_use_code        ,
    land_district_code             ,
    province_state_code            ,
    well_class_code                ,
    well_subclass_guid             ,
    well_yield_unit_code           ,
    latitude                       ,
    longitude                      ,
    ground_elevation               ,
    well_orientation               ,
    other_drilling_method          ,
    drilling_method_code           ,
    ground_elevation_method_code   ,
    well_status_code               ,
    observation_well_number        ,
    obs_well_status_code           ,
    licenced_status_code           ,
    alternative_specifications_ind ,
    construction_start_date        ,
    construction_end_date          ,
    alteration_start_date          ,
    alteration_end_date            ,
    decommission_start_date        ,
    decommission_end_date          ,
    drilling_company_guid          ,
    final_casing_stick_up          ,
    artesian_flow                  ,
    artesian_pressure              ,
    bedrock_depth                  ,
    water_supply_system_name       ,
    water_supply_system_well_name  ,
    well_identification_plate_attached,
    ems                       ,
    screen_intake_method_code ,
    screen_type_code          ,
    screen_material_code      ,
    screen_opening_code       ,
    screen_bottom_code        ,
    utm_zone_code             ,
    utm_northing              ,
    utm_easting               ,
    utm_accuracy_code         ,
    bcgs_id                   ,
    development_method_code   ,
    development_duration      ,
    surface_seal_method_code  ,
    surface_seal_material_code,
    surface_seal_length       ,
    surface_seal_thickness    ,
    backfill_type             ,
    backfill_depth            ,
    liner_material_code       ,
    decommission_reason       ,
    decommission_method_code  ,
    sealant_material          ,
    backfill_material         ,
    decommission_details      ,
    comments                  ,
    create_date               ,
    update_date               ,
    create_user               ,
    update_user)
  SELECT
    wells.well_tag_number                                                    ,
    wells.well_id                                                            ,
    gen_random_uuid()                                                        ,
    wells.acceptance_status_code AS acceptance_status_code                   ,
    concat_ws('' '', owner.giVEN_NAME,OWNER.SURNAME) AS owner_full_name      ,
    concat_ws('' '',OWNER.STREET_NUMBER,STREET_NAME) AS owner_mailing_address,
    owner.city AS owner_city                                                 ,
    owner.postal_code AS owner_postal_code                                   ,
    wells.site_street AS street_address                                      ,
    wells.site_area AS city                                                  ,
    wells.lot_number AS legal_lot                                            ,
    wells.legal_plan AS legal_plan                                           ,
    wells.legal_district_lot AS legal_district_lot                           ,
    wells.legal_block AS legal_block                                         ,
    wells.legal_section AS legal_section                                     ,
    wells.legal_township AS legal_township                                   ,
    wells.legal_range AS legal_range                                         ,
    to_char(wells.pid,''fm000000000'') AS legal_pid                          ,
    wells.well_location AS well_location_description                         ,
    wells.well_identification_plate_no AS identification_plate_number        ,
    wells.diameter AS diameter                                               ,
    wells.total_depth_drilled AS total_depth_drilled                         ,
    wells.depth_well_drilled AS finished_well_depth                          ,
    wells.water_depth                                                        ,
    wells.type_of_well_cap                                                   ,
    CASE wells.well_disinfected_ind
      WHEN ''Y'' THEN TRUE
      WHEN ''N'' THEN FALSE
      ELSE FALSE
    END AS well_disinfected                                                  ,
    wells.yield_value AS well_yield                                          ,
    CASE wells.well_use_code
      WHEN ''OTH'' THEN ''OTHER''
      ELSE wells.well_use_code
    END AS intended_water_use_code                                           ,
    wells.legal_land_district_code as land_district_code                     ,
    CASE owner.province_state_code
      WHEN ''WASH_STATE'' THEN ''WA''
      ELSE owner.province_state_code
    END AS province_state_code                                             ,
    wells.class_of_well_codclassified_by AS well_class_code                ,
    subclass.well_subclass_guid                                            ,
    CASE wells.yield_unit_code
        WHEN ''USGM'' THEN ''USGPM''
        ELSE wells.yield_unit_code
    END AS well_yield_unit_code                          ,
    wells.latitude                                                           ,
    CASE
      WHEN wells.longitude > 0 THEN wells.longitude * -1
      ELSE wells.longitude
    END AS longitude                                                         ,
    wells.elevation AS ground_elevation                                      ,
    CASE wells.orientation_of_well_code
       WHEN ''HORIZ'' THEN false
       ELSE true
    END AS well_orientation                                                  ,
    null AS other_drilling_method, -- placeholder as it is brand new content
    wells.drilling_method_code AS drilling_method_code, -- supersedes CONSTRUCTION_METHOD_CODE
    wells.ground_elevation_method_code AS ground_elevation_method_code,
    CASE wells.status_of_well_code
        WHEN ''UNK'' THEN null -- ''OTHER''
        ELSE wells.status_of_well_code
    END AS well_status_code                                                    ,
    to_char(wells.observation_well_number,''fm000'') AS observation_well_number,
    CASE wells.ministry_observation_well_stat
      WHEN ''Abandoned'' THEN ''Inactive''
      ELSE wells.ministry_observation_well_stat
    END AS obs_well_status_code,
    wells.well_licence_general_status AS licenced_status_code        ,
    CASE wells.alternative_specifications_ind
       WHEN ''N'' THEN false
       WHEN ''Y'' THEN true
       ELSE null
    END AS alternative_specifications_ind              ,
    wells.construction_start_date AT TIME ZONE ''GMT'' ,
    wells.construction_end_date AT TIME ZONE ''GMT''   ,
    wells.alteration_start_date AT TIME ZONE ''GMT''   ,
    wells.alteration_end_date AT TIME ZONE ''GMT''     ,
    wells.closure_start_date AT TIME ZONE ''GMT''      ,
    wells.closure_end_date AT TIME ZONE ''GMT''        ,
    drilling_company.drilling_company_guid             ,
    wells.final_casing_stick_up                        ,
    wells.artesian_flow_value                          ,
    wells.artesian_pressure                            ,
    wells.bedrock_depth                                ,
    wells.water_supply_system_name                     ,
    wells.water_supply_well_name                       ,
    wells.where_plate_attached                         ,
    wells.chemistry_site_id                            ,
    wells.screen_intake_code                           ,
    CASE wells.screen_type_code
        WHEN ''UNK'' THEN null
        ELSE wells.screen_type_code
    END AS screen_type_code                            ,
    CASE wells.screen_material_code
      WHEN ''UNK'' THEN ''OTHER''
      ELSE wells.screen_material_code
    END AS screen_material_code                        ,
    wells.screen_opening_code                          ,
    wells.screen_bottom_code                           ,
    wells.utm_zone_code                                ,
    wells.utm_north                                    ,
    wells.utm_east                                     ,
    wells.utm_accuracy_code                            ,
    wells.bcgs_id                                      ,
    wells.development_method_code                      ,
    wells.development_hours                            ,
    CASE wells.surface_seal_method_code
      WHEN ''UNK'' THEN null
      ELSE wells.surface_seal_method_code
    END AS surface_seal_method_code                    ,
    CASE wells.surface_seal_material_code
      WHEN ''UNK'' THEN ''OTHER''
      ELSE wells.surface_seal_material_code
    END AS surface_seal_material_code                  ,
    wells.surface_seal_depth                           ,
    wells.surface_seal_thickness                       ,
    wells.backfill_type                                ,
    wells.backfill_depth                               ,
    wells.liner_material_code AS liner_material_code   ,
    wells.closure_reason                               ,
    wells.closure_method_code                          ,
    wells.sealant_material                             ,
    wells.backfill_material                            ,
    wells.closure_details                              ,
    wells.general_remarks                              ,
    wells.when_created                                 ,
    COALESCE(wells.when_updated,wells.when_created)    ,
    wells.who_created                                  ,
    COALESCE(wells.who_updated,wells.who_created)
  FROM wells.wells_wells wells LEFT OUTER JOIN wells.wells_owners owner ON owner.owner_id=wells.owner_id
              LEFT OUTER JOIN drilling_company drilling_company ON UPPER(wells.driller_company_code)=UPPER(drilling_company.drilling_company_code)
              LEFT OUTER JOIN well_subclass_code subclass ON UPPER(wells.subclass_of_well_classified_by)=UPPER(subclass.well_subclass_code)
                AND subclass.well_class_code = wells.class_of_well_codclassified_by
  WHERE wells.acceptance_status_code NOT IN (''PENDING'', ''REJECTED'', ''NEW'') ';

BEGIN
  raise notice 'Starting populate_xform() procedure...';

  DROP TABLE IF EXISTS xform_well;
  CREATE unlogged TABLE IF NOT EXISTS xform_well (
     well_tag_number                    integer,
     well_id                            bigint,
     well_guid                          uuid,
     acceptance_status_code             character varying(10),
     owner_full_name                    character varying(200),
     owner_mailing_address              character varying(100),
     owner_city                         character varying(100),
     owner_postal_code                  character varying(10),
     street_address                     character varying(100),
     city                               character varying(50),
     legal_lot                          character varying(10),
     legal_plan                         character varying(20),
     legal_district_lot                 character varying(20),
     legal_block                        character varying(10),
     legal_section                      character varying(10),
     legal_township                     character varying(20),
     legal_range                        character varying(10),
     legal_pid                          character varying(9),
     well_location_description          character varying(500),
     identification_plate_number        integer,
     diameter                           character varying(9),
     total_depth_drilled                numeric(7,2),
     finished_well_depth                numeric(7,2),
     static_water_level                 numeric(7,2),
     well_cap_type                      character varying(40),
     well_disinfected                   boolean,
     well_yield                         numeric(8,3),
     intended_water_use_code            character varying(10),
     land_district_code                 character varying(10),
     province_state_code                character varying(10),
     well_class_code                    character varying(10),
     well_subclass_guid                 uuid,
     well_yield_unit_code               character varying(10),
     latitude                           numeric(8,6),
     longitude                          numeric(9,6),
     ground_elevation                   numeric(10,2),
     well_orientation                   boolean,
     other_drilling_method              character varying(50),
     drilling_method_code               character varying(10),
     ground_elevation_method_code       character varying(10),
     well_status_code                   character varying(10),
     observation_well_number            character varying(3),
     obs_well_status_code               character varying(10),
     licenced_status_code               character varying(10),
     alternative_specifications_ind     boolean,
     construction_start_date            timestamp with time zone,
     construction_end_date              timestamp with time zone,
     alteration_start_date              timestamp with time zone,
     alteration_end_date                timestamp with time zone,
     decommission_start_date            timestamp with time zone,
     decommission_end_date              timestamp with time zone,
     drilling_company_guid              uuid,
     final_casing_stick_up              integer,
     artesian_flow                      numeric(7,2),
     artesian_pressure                  numeric(5,2),
     bedrock_depth                      numeric(7,2),
     well_identification_plate_attached character varying(500),
     water_supply_system_name           character varying(80),
     water_supply_system_well_name      character varying(80),
     ems                                character varying(10),
     screen_intake_method_code          character varying(10),
     screen_type_code                   character varying(10),
     screen_material_code               character varying(10),
     screen_opening_code                character varying(10),
     screen_bottom_code                 character varying(10),
     utm_zone_code                      character varying(10),
     utm_northing                       integer,
     utm_easting                        integer,
     utm_accuracy_code                  character varying(10),
     bcgs_id                            bigint,
     development_method_code            character varying(10),
     development_duration               integer,
     yield_estimation_method_code       character varying(10),
     surface_seal_method_code           character varying(10),
     surface_seal_material_code         character varying(10),
     surface_seal_length                numeric(5,2),
     surface_seal_thickness             numeric(7,2),
     backfill_type                      character varying(250),
     backfill_depth                     numeric(7,2),
     liner_material_code                character varying(10),
     decommission_reason                character varying(250),
     decommission_method_code           character varying(10),
     sealant_material                   character varying(100),
     backfill_material                  character varying(100),
     decommission_details               character varying(250),
     comments                           character varying(255),
     create_date                        timestamp with time zone,
     update_date                        timestamp with time zone,
     create_user                         character varying(30),
     update_user                         character varying(30)
  );

  raise notice 'Created xform_well ETL table';

  IF _subset_ind THEN
    sql_stmt := insert_sql || ' ' || subset_clause;
  ELSE
    sql_stmt := insert_sql;
  END IF;

  raise notice '... transforming wells data (= ACCEPTED) via xform_well ETL table...';
  EXECUTE sql_stmt;

  SELECT count(*) from xform_well into xform_rows;
  raise notice '... % rows loaded into the xform_well table',  xform_rows;
  raise notice 'Finished populate_xform() procedure.';

END;
$$ LANGUAGE plpgsql;
COMMENT ON FUNCTION populate_xform (boolean) IS 'Load ETL Transform Table from legacy Oracle Database using Foreign Data Wrapper.';


-- DESCRIPTION
--   Define the SQL INSERT command that copies from the legacy WELLS_BCGS_NUMBERS table to
--   the analogous GWELLS lookup table (bcgs_number).  Note that the BCGS table isn't strictly
--   a static lookup table as it will be updated with new BCGS mapsheets as they become
--   referenced from new wells in the system.  This happens several times a year.
--
-- PARAMETERS
--   None
--
-- RETURNS
--   None as this is a stored procedure
--
CREATE OR REPLACE FUNCTION migrate_bcgs() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
    raise notice '...importing wells_screens data';

    INSERT INTO bcgs_number (
     create_user, create_date, update_user, update_date, bcgs_id, bcgs_number
    )
    SELECT
     who_created ,when_created ,who_updated ,when_updated, bcgs_id, bcgs_number
    FROM WELLS.WELLS_BCGS_NUMBERS
    ORDER BY BCGS_NUMBER;

    raise notice '...BCGS data imported into the bcgs_number table';
    SELECT count(*) from bcgs_number into row_count;
    raise notice '% rows loaded into the bcgs_number table',  row_count;
END;
$$ LANGUAGE plpgsql;
COMMENT ON FUNCTION migrate_bcgs () IS 'Load BCGS numbers from legacy Oracle Database using Foreign Data Wrapper.';


-- DESCRIPTION
--   Define the SQL INSERT command that copies from the temporary ETL or 'transformation'
--   (i.e. *_xform) table to the main GWELLS 'well' table.
--
-- PARAMETERS
--   None
--
-- RETURNS
--   None as this is a stored procedure
--
CREATE OR REPLACE FUNCTION populate_well() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
  raise notice '... importing transformed WELLS data into the GWELLS main ''well'' table';
  INSERT INTO well (
    well_tag_number             ,
    well_guid                   ,
    owner_full_name             ,
    owner_mailing_address       ,
    owner_city                  ,
    owner_postal_code           ,
    street_address              ,
    city                        ,
    legal_lot                   ,
    legal_plan                  ,
    legal_district_lot          ,
    legal_block                 ,
    legal_section               ,
    legal_township              ,
    legal_range                 ,
    land_district_code          ,
    legal_pid                   ,
    well_location_description   ,
    identification_plate_number ,
    diameter                    ,
    total_depth_drilled         ,
    finished_well_depth         ,
    static_water_level          ,
    well_cap_type               ,
    well_disinfected            ,
    well_yield                  ,
    intended_water_use_code     ,
    province_state_code         ,
    well_class_code             ,
    well_subclass_guid          ,
    well_yield_unit_code        ,
    latitude                    ,
    longitude                   ,
    ground_elevation            ,
    well_orientation            ,
    other_drilling_method       ,
    drilling_method_code        ,
    ground_elevation_method_code,
    create_date                 ,
    update_date                 ,
    create_user                 ,
    update_user                 ,
    surface_seal_length         ,
    surface_seal_thickness      ,
    surface_seal_method_code    ,
    surface_seal_material_code  ,
    backfill_type               ,
    backfill_depth              ,
    liner_material_code         ,
    well_status_code            ,
    observation_well_number     ,
    obs_well_status_code        ,
    licenced_status_code        ,
    other_screen_bottom         ,
    other_screen_material       ,
    development_notes           ,
    water_quality_colour        ,
    water_quality_odour         ,
    alternative_specs_submitted ,
    construction_start_date     ,
    construction_end_date       ,
    alteration_start_date       ,
    alteration_end_date         ,
    decommission_start_date     ,
    decommission_end_date       ,
    drilling_company_guid       ,
    final_casing_stick_up       ,
    artesian_flow               ,
    artesian_pressure           ,
    bedrock_depth               ,
    water_supply_system_name    ,
    water_supply_system_well_name,
    well_identification_plate_attached,
    ems                      ,
    screen_intake_method_code,
    screen_type_code         ,
    screen_material_code     ,
    screen_opening_code      ,
    screen_bottom_code       ,
    utm_zone_code            ,
    utm_northing             ,
    utm_easting              ,
    utm_accuracy_code        ,
    bcgs_id                  ,
    development_method_code  ,
    development_hours        ,
    decommission_reason      ,
    decommission_method_code ,
    sealant_material         ,
    backfill_material        ,
    decommission_details     ,
    comments
    )
  SELECT
    xform.well_tag_number                        ,
    gen_random_uuid()                            ,
    COALESCE(xform.owner_full_name,' ')          ,
    COALESCE(xform.owner_mailing_address, ' ')   ,
    COALESCE(xform.owner_city, ' ')              ,
    COALESCE(xform.owner_postal_code , ' ')      ,
    COALESCE(xform.street_address    , ' ')      ,
    COALESCE(xform.city              , ' ')      ,
    COALESCE(xform.legal_lot         , ' ')      ,
    COALESCE(xform.legal_plan        , ' ')      ,
    COALESCE(xform.legal_district_lot, ' ')      ,
    COALESCE(xform.legal_block       , ' ')      ,
    COALESCE(xform.legal_section     , ' ')      ,
    COALESCE(xform.legal_township    , ' ')      ,
    COALESCE(xform.legal_range       , ' ')      ,
    xform.land_district_code                     ,
    xform.legal_pid                              ,
    COALESCE(xform.well_location_description,' '),
    xform.identification_plate_number            ,
    COALESCE(xform.diameter, ' ')                ,
    xform.total_depth_drilled                    ,
    xform.finished_well_depth                    ,
    xform.static_water_level                     ,
    xform.well_cap_type                          ,
    xform.well_disinfected                       ,
    xform.well_yield                             ,
    xform.intended_water_use_code                ,
    COALESCE(xform.province_state_code,'OTHER')  ,
    xform.well_class_code                   ,
    xform.well_subclass_guid                ,
    xform.well_yield_unit_code              ,
    xform.latitude                          ,
    xform.longitude                         ,
    xform.ground_elevation                  ,
    xform.well_orientation                  ,
    NULL                                    ,
    xform.drilling_method_code              ,
    xform.ground_elevation_method_code      ,
    xform.create_date                       ,
    xform.update_date                       ,
    xform.create_user                       ,
    xform.update_user                       ,
    xform.surface_seal_length               ,
    xform.surface_seal_thickness            ,
    xform.surface_seal_method_code          ,
    xform.surface_seal_material_code        ,
    xform.backfill_type                     ,
    xform.backfill_depth                    ,
    xform.liner_material_code               ,
    xform.well_status_code                  ,
    xform.observation_well_number           ,
    xform.obs_well_status_code              ,
    xform.licenced_status_code              ,
    ''                                      ,
    ''                                      ,
    ''                                      ,
    ''                                      ,
    ''                                      ,
    false                                   ,
    xform.construction_start_date           ,
    xform.construction_end_date             ,
    xform.alteration_start_date             ,
    xform.alteration_end_date               ,
    xform.decommission_start_date           ,
    xform.decommission_end_date             ,
    xform.drilling_company_guid             ,
    xform.final_casing_stick_up             ,
    xform.artesian_flow                     ,
    xform.artesian_pressure                 ,
    xform.bedrock_depth                     ,
    xform.water_supply_system_name          ,
    xform.water_supply_system_well_name     ,
    xform.well_identification_plate_attached,
    xform.ems                               ,
    xform.screen_intake_method_code         ,
    xform.screen_type_code                  ,
    xform.screen_material_code              ,
    xform.screen_opening_code               ,
    xform.screen_bottom_code                ,
    xform.utm_zone_code                     ,
    xform.utm_northing                      ,
    xform.utm_easting                       ,
    xform.utm_accuracy_code                 ,
    xform.bcgs_id                           ,
    xform.development_method_code           ,
    xform.development_duration              ,
    xform.decommission_reason               ,
    xform.decommission_method_code          ,
    xform.sealant_material                  ,
    xform.backfill_material                 ,
    xform.decommission_details              ,
    xform.comments
  FROM xform_well xform;

  raise notice '...xform data imported into the well table';
  SELECT count(*) from well into row_count;
  raise notice '% rows loaded into the well table',  row_count;
END;
$$ LANGUAGE plpgsql;
COMMENT ON FUNCTION populate_well () IS 'Transfer from local XFORM ETL table into well.';


-- DESCRIPTION
--   Define the SQL INSERT command that copies the screen details from the legacy
--   database to the analogous GWELLS table (screen).
--
-- PARAMETERS
--   None
--
-- RETURNS
--   None as this is a stored procedure
--
CREATE OR REPLACE FUNCTION migrate_screens() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
  raise notice '...importing wells_screens data';
  INSERT INTO screen(
    screen_guid                     ,
    filing_number                   ,
    well_tag_number                 ,
    screen_from                     ,
    screen_to                       ,
    internal_diameter               ,
    screen_assembly_type_code       ,
    slot_size                       ,
    create_date                     ,
    update_date                     ,
    create_user                     ,
    update_user)
  SELECT
    gen_random_uuid()               ,
    null                            ,
    xform.well_tag_number           ,
    screens.screen_from             ,
    screens.screen_to               ,
    screens.screen_internal_diameter,
    CASE screens.screen_assembly_type_code
      WHEN 'L'          THEN 'LEAD'
      WHEN 'K  & Riser' THEN 'K_RISER'
      ELSE screens.screen_assembly_type_code
    END AS screen_assembly_type_code,
    screens.screen_slot_size        ,
    screens.when_created            ,
    screens.when_updated            ,
    screens.who_created             ,
    screens.who_updated
  FROM wells.wells_screens screens
  INNER JOIN xform_well xform ON xform.well_id=screens.well_id;

  raise notice '...wells_screens data imported';
  SELECT count(*) from screen into row_count;
  raise notice '% rows loaded into the screen table',  row_count;
END;
$$ LANGUAGE plpgsql;
COMMENT ON FUNCTION migrate_screens () IS 'Load Screen details numbers, only for the wells that have been replicated.';


-- DESCRIPTION
--   Define the SQL INSERT command that copies the production data from the legacy
--   database to the analogous GWELLS table (production_data).
--
-- PARAMETERS
--   None
--
-- RETURNS
--   None as this is a stored procedure
--
CREATE OR REPLACE FUNCTION migrate_production() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
  raise notice '...importing wells_production_data data';
  INSERT INTO production_data(
    production_data_guid         ,
    filing_number                ,
    well_tag_number              ,
    yield_estimation_method_code ,
    yield_estimation_rate        ,
    yield_estimation_duration    ,
    well_yield_unit_code         ,
    static_level                 ,
    drawdown                     ,
    hydro_fracturing_performed   ,
    create_user, create_date     ,
    update_user, update_date
    )
  SELECT
    gen_random_uuid()                                                  ,
    null                                                               ,
    xform.well_tag_number                                              ,
    CASE production_data.yield_estimated_method_code
      WHEN 'UNK' THEN null
      ELSE production_data.yield_estimated_method_code
    END AS yield_estimation_method_code,
    production_data.test_rate                                          ,
    production_data.test_duration                                      ,
    CASE production_data.test_rate_units_code
        WHEN 'USGM' THEN 'USGPM'
        ELSE production_data.test_rate_units_code
    END AS well_yield_unit_code                                        ,
    production_data.static_level                                       ,
    production_data.net_drawdown                                       ,
    false                                                              ,
    production_data.who_created, production_data.when_created,
    COALESCE(production_data.who_updated,production_data.who_created)  ,
    COALESCE(production_data.when_updated,production_data.when_created)
  FROM wells.wells_production_data production_data
  INNER JOIN xform_well xform ON production_data.well_id=xform.well_id;

  raise notice '...wells_production_data data imported';
  SELECT count(*) from production_data into row_count;
  raise notice '% rows loaded into the production_data table',  row_count;
END;
$$ LANGUAGE plpgsql;
COMMENT ON FUNCTION migrate_production () IS 'Load Production Data, only for the wells that have been replicated.';


-- DESCRIPTION
--   Define the SQL INSERT command that copies the casings data from the legacy
--   database to the analogous GWELLS table (casing), referencing well tag number that
--   continues to be used in the new system (table join to the transformation table).
--
-- PARAMETERS
--   None
--
-- RETURNS
--   None as this is a stored procedure
--
CREATE OR REPLACE FUNCTION migrate_casings() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
    raise notice '...importing wells_casings data';
    INSERT INTO casing(
    casing_guid         ,
    filing_number       ,
    well_tag_number     ,
    casing_from         ,
    casing_to           ,
    diameter            ,
    casing_material_code,
    wall_thickness      ,
    drive_shoe          ,
    create_date, update_date, create_user, update_user
    )
    SELECT
        gen_random_uuid()                 ,
        null                              ,
        xform.well_tag_number             ,
        casings.casing_from               ,
        casings.casing_to                 ,
        casings.casing_size               ,
        CASE casings.casing_material_code
          WHEN 'UNK' THEN null
          ELSE casings.casing_material_code
        END AS casing_material_code       ,
        casings.casing_wall               ,
        CASE casings.casing_drive_shoe_ind
            WHEN '' THEN null
            WHEN 'Y' THEN TRUE
            WHEN 'N' THEN FALSE
        END                               ,
        casings.when_created, casings.when_updated, casings.who_created, casings.who_updated
    FROM wells.wells_casings casings
    INNER JOIN xform_well xform ON xform.well_id=casings.well_id;

  raise notice '...wells_casings data imported';
  SELECT count(*) from casing into row_count;
  raise notice '% rows loaded into the casing table',  row_count;
END;
$$ LANGUAGE plpgsql;
COMMENT ON FUNCTION migrate_casings () IS 'Load Casing details, only for the wells that have been replicated.';


-- DESCRIPTION
--   Define the SQL INSERT command that copies the perforation data from the legacy
--   database to the analogous GWELLS table (perforation), referencing well tag number that
--   continues to be used in the new system (table join to the transformation table).
--
--   NOTE: The legacy data has thousands of rows with 'empty' columns; these are
--         filtered out via the SQL WHERE clause.
--
-- PARAMETERS
--   None
--
-- RETURNS
--   None as this is a stored procedure
--
CREATE OR REPLACE FUNCTION migrate_perforations() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
  raise notice '...importing wells_perforations data';
  INSERT INTO perforation(
    perforation_guid                   ,
    well_tag_number                    ,
    liner_thickness                    ,
    liner_diameter                     ,
    liner_from                         ,
    liner_to                           ,
    liner_perforation_from             ,
    liner_perforation_to               ,
    create_user, create_date, update_user, update_date
    )
  SELECT
    gen_random_uuid()                  ,
    xform.well_tag_number              ,
    perforations.liner_thickness       ,
    perforations.liner_diameter        ,
    perforations.liner_from            ,
    perforations.liner_to              ,
    perforations.liner_perforation_from,
    perforations.liner_perforation_to  ,
    perforations.who_created, perforations.when_created, perforations.who_updated, perforations.when_updated
  FROM wells.wells_perforations perforations
  INNER JOIN xform_well xform ON perforations.well_id=xform.well_id
  WHERE NOT (liner_from is  null
  AND liner_to               IS  NULL
  AND liner_diameter         IS  NULL
  AND liner_thickness        IS  NULL
  AND liner_perforation_from IS  NULL
  AND liner_perforation_to   IS  NULL);

  raise notice '...wells_perforations data imported';
  SELECT count(*) from perforation into row_count;
  raise notice '% rows loaded into the perforation table',  row_count;
END;
$$ LANGUAGE plpgsql;
COMMENT ON FUNCTION migrate_perforations () IS 'Load BCGS numbers, only for the wells that have been replicated.';


-- DESCRIPTION
--   Define the SQL INSERT command that copies the aquifer linkages from the legacy
--   database to the analogous GWELLS table (aquifer_well), referencing well tag number that
--   continues to be used in the new system (table join to the transformation table).
--
-- PARAMETERS
--   None
--
-- RETURNS
--   None as this is a stored procedure
--
CREATE OR REPLACE FUNCTION migrate_aquifers() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
  raise notice '...importing gw_aquifer_wells data';

  INSERT INTO aquifer_well(
    aquifer_well_guid,
    aquifer_id,
    well_tag_number,
    create_user,create_date,update_user,update_date
    )
  SELECT
    gen_random_uuid()    ,
    aws.aquifer_id       ,
    xform.well_tag_number,
    aws.who_created      ,
    aws.when_created     ,
    coalesce(aws.who_updated, aws.who_created),
    coalesce(aws.when_updated,aws.when_created)
  FROM wells.gw_aquifer_wells aws INNER JOIN xform_well xform ON aws.well_id = xform.well_id;

  raise notice '...gw_aquifer_well data imported';
  SELECT count(*) from aquifer_well into row_count;
  raise notice '% rows loaded into the aquifer_well table',  row_count;
END;
$$ LANGUAGE plpgsql;
COMMENT ON FUNCTION migrate_aquifers () IS 'Load Aquifer Wells, only for the wells that have been replicated.';

-- DESCRIPTION
--   Define the SQL INSERT command that copies the lithology from the legacy
--   database to the analogous GWELLS table (lithology_description), referencing well tag
--   number that continues to be used in the new system (table join to the transformation
--   table).
--
--   NOTE: This copy also converts the flow units ('USGM'to 'USGPM').

-- PARAMETERS
--   None
--
-- RETURNS
--   None as this is a stored procedure
--
CREATE OR REPLACE FUNCTION migrate_lithology() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
  raise notice '...importing wells_lithology_descriptions data';

  INSERT INTO lithology_description(
    lithology_description_guid  ,
    filing_number               ,
    well_tag_number             ,
    lithology_from              ,
    lithology_to                ,
    lithology_raw_data          ,
    lithology_description_code  ,
    lithology_material_code     ,
    lithology_hardness_code     ,
    lithology_colour_code       ,
    water_bearing_estimated_flow,
    well_yield_unit_code        ,
    lithology_observation       ,
    lithology_sequence_number   ,
    create_user, create_date, update_user, update_date
    )
  SELECT
    gen_random_uuid()                ,
    null                             ,
    xform.well_tag_number            ,
    wld.lithology_from               ,
    wld.lithology_to                 ,
    wld.lithology_raw_data           ,
    wld.lithology_code               ,
    wld.lithology_material_code      ,
    wld.relative_hardness_code       ,
    wld.lithology_colour_code        ,
    wld.water_bearing_estimated_flow ,
    CASE wld.water_bearing_est_flw_unt_cd
        WHEN 'USGM' THEN 'USGPM'
        ELSE wld.water_bearing_est_flw_unt_cd
    END AS well_yield_unit_code      ,
    wld.lithology_observation        ,
    wld.lithology_sequence_number    ,
    wld.who_created, wld.when_created, COALESCE(wld.who_updated, wld.who_created), COALESCE(wld.when_updated, wld.when_created)
  FROM wells.wells_lithology_descriptions wld
  INNER JOIN xform_well xform ON xform.well_id=wld.well_id
  INNER JOIN wells.wells_wells wells ON wells.well_id=wld.well_id;

  raise notice '...wells_lithology_descriptions data imported';
  SELECT count(*) from lithology_description into row_count;
  raise notice '% rows loaded into the lithology_description table',  row_count;
END;
$$ LANGUAGE plpgsql;
COMMENT ON FUNCTION migrate_lithology () IS 'Load Lithology, only for the wells that have been replicated.';


-- DESCRIPTION
--   Define two driver stored procedures, grouping the SQL commands that runs the WELLS to
--   GWELLS replication, into two distinct steps.  This does NOT include a refresh of the
--   static code tables; that is done only during the pipeline build and deploy.
--
--   This division (into two steps) of the WELLS to GWELLS replication, is required to work
--   around an intermittent postgresql bug; for more details see:
--   https://github.com/bcgov/gwells/wiki/Regular-Corruption-of-the-PostgreSQL-DB
--
--   There is the opportunity to run 'VACUUM FULL' to reclaim disk space, in between
--   these two steps.
--
--   These steps will succeed only if the static code tables are already populated.
--
--   NOTE: This procedure is meant to be run from the Database Pod, during scheduled nightly
--         replications or on an ad-hoc fashion. It is not part of a pipeline build or deployment.
--
-- USAGE
--  1. If run from a terminal window on the postgresql pod (the $POSTGRESQL_* environment variables
--     are guaranteed to be set correctly on the pod).  For example:
--
--     psql -t -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c 'SELECT db_replicate_step1(_subset_ind=>false);'
--     psql -t -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c 'SELECT db_replicate_step2;'
--
--  2. If invoked remotely from a developer workstation, on the postgresql pod (the quotes and double-quotes
--     are required, and the pod name will vary with each deployment. For example:
--
--    oc exec postgresql-80-04n7h -- /bin/bash -c 'psql -t -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c "SELECT db_replicate_step1(_subset_ind=>false);"'
--    oc exec postgresql-80-04n7h -- /bin/bash -c 'psql -t -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c "SELECT db_replicate_step2"'
--
--
--  3. If run on the local environment of a developer workstation, replace the password and username with the
--     local credentials, or ensure that the $POSTGRESQL_* environment variables are set correctly to point
--     to the local database. For example:
--
--     psql -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c 'SELECT db_replicate_step1(_subset_ind=>true);'
--     psql -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c 'SELECT db_replicate_step2;'
--
CREATE OR REPLACE FUNCTION db_replicate_step1(_subset_ind boolean default true) RETURNS void AS $$
BEGIN
  raise notice 'Replicating WELLS to GWELLS.';
  raise notice '.. step 1 (of 2)';

  PERFORM populate_xform(_subset_ind);
  TRUNCATE TABLE bcgs_number CASCADE;
  PERFORM migrate_bcgs();
  TRUNCATE TABLE well CASCADE;
  PERFORM populate_well();
  PERFORM migrate_screens();
  PERFORM migrate_production();
END;
$$ LANGUAGE plpgsql;
COMMENT ON FUNCTION db_replicate_step1 (boolean) IS 'SQL Driver script to run replication, without code table refresh (step 1).';

CREATE OR REPLACE FUNCTION db_replicate_step2 () RETURNS void AS $$
BEGIN
  raise notice 'Replicating WELLS to GWELLS.';
  raise notice '.. step 2 (of 2)';
  PERFORM migrate_casings();
  PERFORM migrate_perforations();
  PERFORM migrate_aquifers();
  PERFORM migrate_lithology();
  DROP TABLE IF EXISTS xform_well;
  raise notice 'Finished replicating WELLS to GWELLS.';
END;
$$ LANGUAGE plpgsql;
COMMENT ON FUNCTION db_replicate_step2 () IS 'SQL Driver script to run replication, without code table refresh (step 2).';
