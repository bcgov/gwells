DROP FUNCTION IF EXISTS populate_xform(boolean);

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
        WHEN ''UNK'' THEN ''OTHER''
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
        WHEN ''UNK'' THEN ''OTHER''
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
      WHEN ''UNK'' THEN ''OTHER''
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
     well_tag_number                     integer,
     well_id                             bigint,
     well_guid                           uuid,
     acceptance_status_code              character varying(10),
     owner_full_name                     character varying(200),
     owner_mailing_address               character varying(100),
     owner_city                          character varying(100),
     owner_postal_code                   character varying(10),
     street_address                      character varying(100),
     city                                character varying(50),
     legal_lot                           character varying(10),
     legal_plan                          character varying(20),
     legal_district_lot                  character varying(20),
     legal_block                         character varying(10),
     legal_section                       character varying(10),
     legal_township                      character varying(20),
     legal_range                         character varying(10),
     legal_pid                           character varying(9),
     well_location_description           character varying(500),
     identification_plate_number         integer,
     diameter                            character varying(9),
     total_depth_drilled                 numeric(7,2),
     finished_well_depth                 numeric(7,2),
     static_water_level                  numeric(7,2),
     well_cap_type                       character varying(40),
     well_disinfected                    boolean,
     well_yield                          numeric(8,3),
     intended_water_use_code             character varying(10),
     land_district_code                  character varying(10),
     province_state_code                 character varying(10),
     well_class_code                     character varying(10),
     well_subclass_guid                  uuid,
     well_yield_unit_code                character varying(10),
     latitude                            numeric(8,6),
     longitude                           numeric(9,6),
     ground_elevation                    numeric(10,2),
     well_orientation                    boolean,
     other_drilling_method               character varying(50),
     drilling_method_code                character varying(10),
     ground_elevation_method_code        character varying(10),
     well_status_code                    character varying(10),
     observation_well_number             character varying(3),
     obs_well_status_code                character varying(10),
     licenced_status_code                character varying(10),
     alternative_specifications_ind      boolean,
     construction_start_date             timestamp with time zone,
     construction_end_date               timestamp with time zone,
     alteration_start_date               timestamp with time zone,
     alteration_end_date                 timestamp with time zone,
     decommission_start_date             timestamp with time zone,
     decommission_end_date               timestamp with time zone,
     drilling_company_guid               uuid,
     final_casing_stick_up               integer,
     artesian_flow                       numeric(7,2),
     artesian_pressure                   numeric(5,2),
     bedrock_depth                       numeric(7,2),
     well_identification_plate_attached character varying(500),
     water_supply_system_name            character varying(80),
     water_supply_system_well_name       character varying(80),
     ems                                 character varying(10),
     screen_intake_method_code           character varying(10),
     screen_type_code                    character varying(10),
     screen_material_code                character varying(10),
     screen_opening_code                 character varying(10),
     screen_bottom_code                  character varying(10),
     utm_zone_code                       character varying(10),
     utm_northing                        integer,
     utm_easting                         integer,
     utm_accuracy_code                   character varying(10),
     bcgs_id                             bigint,
     development_method_code             character varying(10),
     development_duration                integer,
     yield_estimation_method_code        character varying(10),
     surface_seal_method_code            character varying(10),
     surface_seal_material_code          character varying(10),
     surface_seal_length                 numeric(5,2),
     surface_seal_thickness              numeric(7,2),
     backfill_type                       character varying(250),
     backfill_depth                      numeric(7,2),
     liner_material_code                 character varying(10),
     decommission_reason                 character varying(250),
     decommission_method_code            character varying(10),
     sealant_material                    character varying(100),
     backfill_material                   character varying(100),
     decommission_details                character varying(250),
     comments                            character varying(255),
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
