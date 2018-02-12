DROP FUNCTION IF EXISTS gwells_populate_xform(boolean);

CREATE OR REPLACE FUNCTION gwells_populate_xform(
  _subset_ind boolean DEFAULT true) RETURNS void AS $$
DECLARE
  xform_rows integer;
  sql_stmt text;
  subset_clause text := 'AND wells.well_tag_number between 100001 and 113567';
  insert_sql    text := 'INSERT INTO xform_gwells_well (
    well_tag_number                    ,
    well_id                            ,
    well_guid                          ,
    acceptance_status_code             ,
    owner_full_name                    ,
    owner_mailing_address              ,
    owner_city                         ,
    owner_postal_code                  ,
    street_address                     ,
    city                               ,
    legal_lot                          ,
    legal_plan                         ,
    legal_district_lot                 ,
    legal_block                        ,
    legal_section                      ,
    legal_township                     ,
    legal_range                        ,
    legal_pid                          ,
    well_location_description          ,
    identification_plate_number        ,
    diameter                           ,
    total_depth_drilled                ,
    finished_well_depth                ,
    static_water_level                 ,
    well_cap_type                      ,
    well_disinfected                   ,
    well_yield                         ,
    intended_water_use_guid            ,
    land_district_guid                 ,
    province_state_guid                ,
    well_class_guid                    ,
    well_subclass_guid                 ,
    well_yield_unit_guid               ,
    latitude                           ,
    longitude                          ,
    ground_elevation                   ,
    well_orientation                   ,
    other_drilling_method              ,
    drilling_method_guid               ,
    ground_elevation_method_guid       ,
    well_status_guid                   ,
    observation_well_number            ,
    observation_well_status_guid       ,
    licenced_status_guid               ,
    alternative_specifications_ind     ,
    construction_start_date            ,
    construction_end_date              ,
    alteration_start_date              ,
    alteration_end_date                ,
    decommission_start_date            ,
    decommission_end_date              ,
    drilling_company_guid              ,
    final_casing_stick_up              ,
    artesian_flow                      ,
    artesian_pressure                  ,
    bedrock_depth                      ,
    water_supply_system_name           ,
    water_supply_system_well_name      ,
    well_identification_plate_attached ,
    ems                                ,
    screen_intake_method_guid          ,
    screen_type_guid                   ,
    screen_material_guid               ,
    screen_opening_guid                ,
    screen_bottom_guid                 ,
    utm_zone_code                      ,
    utm_northing                       ,
    utm_easting                        ,
    utm_accuracy_code                  ,
    bcgs_id                            ,
    development_method_guid            ,
    development_duration               ,
    surface_seal_method_guid           ,
    surface_seal_material_guid         ,
    surface_seal_length                ,
    surface_seal_thickness             ,
    backfill_type                      ,
    backfill_depth                     ,
    liner_material_guid                ,
    decommission_reason                ,
    decommission_method_guid           ,
    sealant_material                   ,
    backfill_material                  ,
    decommission_details               ,
    comments                           ,
    create_date                       ,
    update_date                       ,
    create_user                        ,
    update_user)
  SELECT
    wells.well_tag_number                                                    ,
    wells.well_id                                                            ,
    gen_random_uuid()                                                        ,
    wells.acceptance_status_code AS acceptance_status_code                   ,
    concat_ws('' '', owner.giVEN_NAME,OWNER.SURNAME) AS owner_full_name        ,
    concat_ws('' '',OWNER.STREET_NUMBER,STREET_NAME) AS owner_mailing_address  ,
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
    to_char(wells.pid,''fm000000000'') AS legal_pid                            ,
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
    intended_water_use.intended_water_use_guid                               ,
    gld.land_district_guid                                                   ,
    CASE owner.province_state_code
      WHEN ''BC'' THEN ''f46b70b647d411e7a91992ebcb67fe33''::uuid
      WHEN ''AB'' THEN ''f46b742647d411e7a91992ebcb67fe33''::uuid
      WHEN ''WASH_STATE'' THEN ''f46b77b447d411e7a91992ebcb67fe33''::uuid
      ELSE ''f46b7b1a47d411e7a91992ebcb67fe33''::uuid
    END AS province_state_guid                                             ,
    class.well_class_guid                                                  ,
    subclass.well_subclass_guid                                            ,
    CASE wells.yield_unit_code
      WHEN ''GPM''  THEN ''c4634ef447c311e7a91992ebcb67fe33''::uuid
      WHEN ''IGM''  THEN ''c4634ff847c311e7a91992ebcb67fe33''::uuid
      WHEN ''DRY''  THEN ''c46347b047c311e7a91992ebcb67fe33''::uuid
      WHEN ''LPS''  THEN ''c46350c047c311e7a91992ebcb67fe33''::uuid
      WHEN ''USGM'' THEN ''c463525047c311e7a91992ebcb67fe33''::uuid
      WHEN ''GPH''  THEN ''c4634b4847c311e7a91992ebcb67fe33''::uuid
      WHEN ''UNK''  THEN ''c463518847c311e7a91992ebcb67fe33''::uuid
      ELSE ''c463518847c311e7a91992ebcb67fe33''::uuid -- As PostgreSQL does not permit "" as guid value
    END AS well_yield_unit_guid                                              ,
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
    CASE wells.drilling_method_code  -- supersedes CONSTRUCTION_METHOD_CODE
      WHEN ''AIR_ROTARY'' THEN ''262aca1e5db211e7907ba6006ad3dba0''::uuid
      WHEN ''AUGER''      THEN ''262ace565db211e7907ba6006ad3dba0''::uuid
      WHEN ''CABLE_TOOL'' THEN ''262ad3d85db211e7907ba6006ad3dba0''::uuid
      WHEN ''DRIVING''    THEN ''262ad54a5db211e7907ba6006ad3dba0''::uuid
      WHEN ''DUGOUT''     THEN ''262ad6265db211e7907ba6006ad3dba0''::uuid
      WHEN ''DUO_ROTARY'' THEN ''262ad6ee5db211e7907ba6006ad3dba0''::uuid
      WHEN ''EXCAVATING'' THEN ''262ad7b65db211e7907ba6006ad3dba0''::uuid
      WHEN ''JETTING''    THEN ''262adb445db211e7907ba6006ad3dba0''::uuid
      WHEN ''MUD_ROTARY'' THEN ''262adc2a5db211e7907ba6006ad3dba0''::uuid
      WHEN ''OTHER''      THEN ''262adcf25db211e7907ba6006ad3dba0''::uuid
      WHEN ''UNK''        THEN ''262addb05db211e7907ba6006ad3dba0''::uuid
      ELSE null::uuid
    END AS drilling_method_guid                                              ,
    CASE wells.ground_elevation_method_code
      WHEN ''5K_MAP''  THEN ''523ac3ba77ad11e7b5a5be2e44b06b34''::uuid
      WHEN ''10K_MAP''  THEN ''523ac81077ad11e7b5a5be2e44b06b34''::uuid
      WHEN ''20K_MAP''  THEN ''523aca0477ad11e7b5a5be2e44b06b34''::uuid
      WHEN ''50K_MAP''  THEN ''523ad10277ad11e7b5a5be2e44b06b34''::uuid
      WHEN ''ALTIMETER'' THEN ''523ad2d877ad11e7b5a5be2e44b06b34''::uuid
      WHEN ''DIFF_GPS''  THEN ''523ad47277ad11e7b5a5be2e44b06b34''::uuid
      WHEN ''GPS''  THEN ''523ad60277ad11e7b5a5be2e44b06b34''::uuid
      WHEN ''LEVEL''  THEN ''523ad79277ad11e7b5a5be2e44b06b34''::uuid
      ELSE null::uuid
    END AS ground_elevation_method_guid                                      ,
    well_status.well_status_guid                                             ,
    to_char(wells.observation_well_number,''fm000'') AS observation_well_number,
    CASE wells.ministry_observation_well_stat
      WHEN ''Inactive'' THEN ''b703a326-8ecc-48e4-89dd-d2fbd58834a9''::uuid
      WHEN ''Active'' THEN ''1af7ba78-1ab6-4992-b4f6-f105e519d2a6''::uuid
      ELSE null::uuid
    END AS observation_well_status_guid                                      ,
    licenced_status.licenced_status_guid                                     ,
    CASE wells.alternative_specifications_ind
       WHEN ''N'' THEN false
       WHEN ''Y'' THEN true
       ELSE null
    END AS alternative_specifications_ind                                    ,
    wells.construction_start_date AT TIME ZONE ''GMT''                         ,
    wells.construction_end_date AT TIME ZONE ''GMT''                           ,
    wells.alteration_start_date AT TIME ZONE ''GMT''                           ,
    wells.alteration_end_date AT TIME ZONE ''GMT''                             ,
    wells.closure_start_date AT TIME ZONE ''GMT''                              ,
    wells.closure_end_date AT TIME ZONE ''GMT''                                ,
    drilling_company.drilling_company_guid                                   ,
    wells.final_casing_stick_up                                              ,
    wells.artesian_flow_value                                                ,
    wells.artesian_pressure                                                  ,
    wells.bedrock_depth                                                      ,
    wells.water_supply_system_name                                           ,
    wells.water_supply_well_name                                             ,
    wells.where_plate_attached                                               ,
    wells.chemistry_site_id                                                  ,
    screen_intake_method.screen_intake_method_guid                           ,
    screen_type.screen_type_guid                                             ,
    screen_material.screen_material_guid                                     ,
    screen_opening.screen_opening_guid                                       ,
    screen_bottom.screen_bottom_guid                                         ,
    wells.utm_zone_code                                                      ,
    wells.utm_north                                                          ,
    wells.utm_east                                                           ,
    wells.utm_accuracy_code                                                  ,
    wells.bcgs_id                                                            ,
    development_method.development_method_guid                               ,
    wells.development_hours                                                  ,
    surface_seal_method.surface_seal_method_guid                             ,
    surface_seal_material.surface_seal_material_guid                         ,
    wells.surface_seal_depth                                                 ,
    wells.surface_seal_thickness                                             ,
    wells.backfill_type                                                      ,
    wells.backfill_depth                                                     ,
    liner_material.liner_material_guid                                       ,
    wells.closure_reason                                                     ,
    decommission_method.decommission_method_guid                             ,
    wells.sealant_material                                                   ,
    wells.backfill_material                                                  ,
    wells.closure_details                                                    ,
    wells.general_remarks                                                    ,
    wells.when_created                                                       ,
    COALESCE(wells.when_updated,wells.when_created)                          ,
    wells.who_created                                                        ,
    COALESCE(wells.who_updated,wells.who_created)
  FROM wells.wells_wells wells LEFT OUTER JOIN wells.wells_owners owner ON owner.owner_id=wells.owner_id
              LEFT OUTER JOIN drilling_company drilling_company ON UPPER(wells.driller_company_code)=UPPER(drilling_company.drilling_company_code)
              LEFT OUTER JOIN gwells_screen_intake_method screen_intake_method ON UPPER(wells.screen_intake_code)=UPPER(screen_intake_method.screen_intake_code)
              LEFT OUTER JOIN gwells_screen_type screen_type ON UPPER(wells.screen_type_code)=UPPER(screen_type.screen_type_code)
              LEFT OUTER JOIN gwells_screen_material screen_material ON UPPER(wells.screen_material_code)=UPPER(screen_material.screen_material_code)
              LEFT OUTER JOIN gwells_screen_opening screen_opening ON UPPER(wells.screen_opening_code)=UPPER(screen_opening.screen_opening_code)
              LEFT OUTER JOIN gwells_screen_bottom screen_bottom ON UPPER(wells.screen_bottom_code)=UPPER(screen_bottom.screen_bottom_code)
              LEFT OUTER JOIN development_method_code development_method ON UPPER(wells.development_method_code)=UPPER(development_method.development_method_code)
              LEFT OUTER JOIN gwells_surface_seal_method surface_seal_method ON UPPER(wells.surface_seal_method_code)=UPPER(surface_seal_method.surface_seal_method_code)
              LEFT OUTER JOIN gwells_surface_seal_material surface_seal_material ON UPPER(wells.surface_seal_material_code)=UPPER(surface_seal_material.surface_seal_material_code)
              LEFT OUTER JOIN liner_material_code liner_material ON UPPER(wells.liner_material_code)=UPPER(liner_material.liner_material_code)
              LEFT OUTER JOIN land_district_code gld ON UPPER(wells.legal_land_district_code)=UPPER(gld.code)
              LEFT OUTER JOIN gwells_well_status well_status ON UPPER(wells.status_of_well_code)=UPPER(well_status.code)
              LEFT OUTER JOIN licenced_status_code licenced_status ON UPPER(wells.well_licence_general_status)=UPPER(licenced_status.code)
              LEFT OUTER JOIN intended_water_use_code intended_water_use ON UPPER(wells.well_use_code)=UPPER(intended_water_use.code)
              LEFT OUTER JOIN gwells_well_class class ON UPPER(wells.class_of_well_codclassified_by)=UPPER(class.code)
              LEFT OUTER JOIN gwells_well_subclass subclass ON UPPER(wells.subclass_of_well_classified_by)=UPPER(subclass.code) AND subclass.well_class_guid = class.well_class_guid
              LEFT OUTER JOIN decommission_method_code decommission_method ON UPPER(wells.closure_method_code)=UPPER(decommission_method.code)
  WHERE wells.acceptance_status_code NOT IN (''PENDING'', ''REJECTED'', ''NEW'') ';

BEGIN
  raise notice 'Starting gwells_populate_xform() procedure...';

  DROP TABLE IF EXISTS xform_gwells_well;
  CREATE unlogged TABLE IF NOT EXISTS xform_gwells_well (
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
     intended_water_use_guid             uuid,
     land_district_guid                  uuid,
     province_state_guid                 uuid,
     well_class_guid                     uuid,
     well_subclass_guid                  uuid,
     well_yield_unit_guid                uuid,
     latitude                            numeric(8,6),
     longitude                           numeric(9,6),
     ground_elevation                    numeric(10,2),
     well_orientation                    boolean,
     other_drilling_method               character varying(50),
     drilling_method_guid                uuid,
     ground_elevation_method_guid        uuid,
     well_status_guid                    uuid,
     observation_well_number             character varying(3),
     observation_well_status_guid        uuid,
     licenced_status_guid                uuid,
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
     screen_intake_method_guid           uuid,
     screen_type_guid                    uuid,
     screen_material_guid                uuid,
     screen_opening_guid                 uuid,
     screen_bottom_guid                  uuid,
     utm_zone_code                       character varying(10),
     utm_northing                        integer,
     utm_easting                         integer,
     utm_accuracy_code                   character varying(10),
     bcgs_id                             bigint,
     development_method_guid             uuid,
     development_duration                integer,
     yield_estimation_method_guid        uuid,
     surface_seal_method_guid            uuid,
     surface_seal_material_guid          uuid,
     surface_seal_length                 numeric(5,2),
     surface_seal_thickness              numeric(7,2),
     backfill_type                       character varying(250),
     backfill_depth                      numeric(7,2),
     liner_material_guid                 uuid,
     decommission_reason                 character varying(250),
     decommission_method_guid            uuid,
     sealant_material                    character varying(100),
     backfill_material                   character varying(100),
     decommission_details                character varying(250),
     comments                            character varying(255),
     create_date                        timestamp with time zone,
     update_date                        timestamp with time zone,
     create_user                         character varying(30),
     update_user                         character varying(30)
  );

  raise notice 'Created xform_gwells_well ETL table';

  IF _subset_ind THEN
    sql_stmt := insert_sql || ' ' || subset_clause;
  ELSE
    sql_stmt := insert_sql;
  END IF;

  raise notice '... transforming wells data (= ACCEPTED) via xform_gwells_well ETL table...';
  EXECUTE sql_stmt;

  SELECT count(*) from xform_gwells_well into xform_rows;
  raise notice '... % rows loaded into the xform_gwells_well table',  xform_rows;
  raise notice 'Finished gwells_populate_xform() procedure.';

END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION gwells_populate_xform (boolean) IS 'Load ETL Transform Table from legacy Oracle Database using Foreign Data Wrapper.';
