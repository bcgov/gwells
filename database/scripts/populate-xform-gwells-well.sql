DROP FUNCTION IF EXISTS populate_xform_gwells_well();
-- Must be run as PostgreSQL admin due to the 'copy' commands (i.e. psql -d gwells)
CREATE OR REPLACE FUNCTION populate_xform_gwells_well() RETURNS void AS $$

DECLARE

xform_rows integer;

BEGIN
  raise notice 'Starting populate_xform_gwells_well() procedure...';
  raise notice '... transforming wells data (!= REJECTED) via xform_gwells_well ETL table...';

  INSERT INTO xform_gwells_well (
    well_tag_number                    ,
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
    well_yield                         ,
    well_use_code                      ,
    legal_land_district_code           ,
    province_state_guid                ,
    class_of_well_codclassified_by     ,
    subclass_of_well_classified_by     ,
    well_yield_unit_guid               ,
    latitude                           ,
    longitude                          ,
    ground_elevation                   ,
    well_orientation                   ,
    other_drilling_method              ,
    drilling_method_guid               ,
    ground_elevation_method_guid       ,
    bkfill_above_srfc_seal_depth       ,
    backfill_above_surface_seal        ,
    sealant_material                   ,
    status_of_well_code                ,
    observation_well_number            ,
    ministry_observation_well_stat     ,
    well_licence_general_status        ,
    alternative_specifications_ind     ,
    construction_start_date            ,
    construction_end_date              ,
    alteration_start_date              ,
    alteration_end_date                ,
    decommission_start_date            ,
    decommission_end_date              ,
    /*drilling_company_guid          ,*/
    final_casing_stick_up              ,
    artesian_flow                      ,
    artesian_pressure                  ,
    bedrock_depth                      ,
    well_identification_plate_attached ,
    when_created                       ,
    when_updated                       ,
    who_created                        ,
    who_updated)
  SELECT
    WELLS.WELL_TAG_NUMBER                                                  ,
    null                                                                   , -- gen_random_uuid()  AS WELL_GUID,
    WELLS.ACCEPTANCE_STATUS_CODE AS acceptance_status_code                 ,
    concat_ws(' ', owner.giVEN_NAME,OWNER.SURNAME) AS owner_full_name      ,
    concat_ws(' ',OWNER.STREET_NUMBER,STREET_NAME) AS owner_mailing_address,
    OWNER.CITY AS owner_city                                               ,
    OWNER.POSTAL_CODE AS owner_postal_code                                 ,
    WELLS.SITE_STREET AS street_address                                    ,
    WELLS.SITE_AREA AS city                                                ,
    WELLS.LOT_NUMBER AS legal_lot                                          ,
    WELLS.LEGAL_PLAN AS legal_plan                                         ,
    WELLS.LEGAL_DISTRICT_LOT AS legal_district_lot                         ,
    WELLS.LEGAL_BLOCK AS legal_block                                       ,
    WELLS.LEGAL_SECTION AS legal_section                                   ,
    WELLS.LEGAL_TOWNSHIP AS legal_township                                 ,
    WELLS.LEGAL_RANGE AS legal_range                                       ,
    WELLS.PID AS legal_pid                                                 ,
    WELLS.WELL_LOCATION AS well_location_description                       ,
    WELLS.WELL_IDENTIFICATION_PLATE_NO AS identification_plate_number      ,
    WELLS.DIAMETER AS diameter                                             ,
    WELLS.TOTAL_DEPTH_DRILLED AS total_depth_drilled                       ,
    WELLS.DEPTH_WELL_DRILLED AS finished_well_depth                        ,
    WELLS.YIELD_VALUE AS well_yield                                        ,
    WELLS.WELL_USE_CODE                                                    , -- -> intended_water_use_guid
    WELLS.LEGAL_LAND_DISTRICT_CODE                                         , -- -> legal_land_district_guid
    CASE OWNER.PROVINCE_STATE_CODE
      WHEN 'BC' THEN 'f46b70b647d411e7a91992ebcb67fe33'::uuid
      WHEN 'AB' THEN 'f46b742647d411e7a91992ebcb67fe33'::uuid
      WHEN 'WASH_STATE' THEN 'f46b77b447d411e7a91992ebcb67fe33'::uuid
      ELSE 'f46b7b1a47d411e7a91992ebcb67fe33'::uuid
    END AS province_state_guid                                             ,
    coalesce (WELLS.CLASS_OF_WELL_CODCLASSIFIED_BY,'LEGACY')               ,
    WELLS.SUBCLASS_OF_WELL_CLASSIFIED_BY                                   , -- -> well_subclass_guid
    CASE WELLS.YIELD_UNIT_CODE
      WHEN 'GPM'  THEN 'c4634ef447c311e7a91992ebcb67fe33'::uuid
      WHEN 'IGM'  THEN 'c4634ff847c311e7a91992ebcb67fe33'::uuid
      WHEN 'DRY'  THEN 'c46347b047c311e7a91992ebcb67fe33'::uuid
      WHEN 'LPS'  THEN 'c46350c047c311e7a91992ebcb67fe33'::uuid
      WHEN 'USGM' THEN 'c463525047c311e7a91992ebcb67fe33'::uuid
      WHEN 'GPH'  THEN 'c4634b4847c311e7a91992ebcb67fe33'::uuid
      WHEN 'UNK'  THEN 'c463518847c311e7a91992ebcb67fe33'::uuid
      ELSE 'c463518847c311e7a91992ebcb67fe33'::uuid -- As PostGres didn't like "" as guid value
    END AS well_yield_unit_guid                                            ,
    WELLS.LATITUDE                                                         ,
    CASE
      WHEN WELLS.LONGITUDE > 0 THEN WELLS.LONGITUDE * -1
      ELSE WELLS.LONGITUDE
    END AS longitude                                                       ,
    WELLS.ELEVATION AS ground_elevation                                    ,
    CASE WELLS.ORIENTATION_OF_WELL_CODE
       WHEN 'HORIZ' THEN false
       ELSE true
    END AS well_orientation                                                ,
    null AS other_drilling_method, -- placeholder as it's brand new content
    CASE WELLS.DRILLING_METHOD_CODE  -- supersedes CONSTRUCTION_METHOD_CODE
      WHEN 'AIR_ROTARY' THEN '262aca1e5db211e7907ba6006ad3dba0'::uuid
      WHEN 'AUGER'      THEN '262ace565db211e7907ba6006ad3dba0'::uuid
      WHEN 'CABLE_TOOL' THEN '262ad3d85db211e7907ba6006ad3dba0'::uuid
      WHEN 'DRIVING'    THEN '262ad54a5db211e7907ba6006ad3dba0'::uuid
      WHEN 'DUGOUT'     THEN '262ad6265db211e7907ba6006ad3dba0'::uuid
      WHEN 'DUO_ROTARY' THEN '262ad6ee5db211e7907ba6006ad3dba0'::uuid
      WHEN 'EXCAVATING' THEN '262ad7b65db211e7907ba6006ad3dba0'::uuid
      WHEN 'JETTING'    THEN '262adb445db211e7907ba6006ad3dba0'::uuid
      WHEN 'MUD_ROTARY' THEN '262adc2a5db211e7907ba6006ad3dba0'::uuid
      WHEN 'OTHER'      THEN '262adcf25db211e7907ba6006ad3dba0'::uuid
      WHEN 'UNK'        THEN '262addb05db211e7907ba6006ad3dba0'::uuid
      ELSE null::uuid
    END AS drilling_method_guid                                            ,
    CASE WELLS.GROUND_ELEVATION_METHOD_CODE
      WHEN '5K_MAP'  THEN '523ac3ba77ad11e7b5a5be2e44b06b34'::uuid
      WHEN '10K_MAP'  THEN '523ac81077ad11e7b5a5be2e44b06b34'::uuid
      WHEN '20K_MAP'  THEN '523aca0477ad11e7b5a5be2e44b06b34'::uuid
      WHEN '50K_MAP'  THEN '523ad10277ad11e7b5a5be2e44b06b34'::uuid
      WHEN 'ALTIMETER' THEN '523ad2d877ad11e7b5a5be2e44b06b34'::uuid
      WHEN 'DIFF_GPS'  THEN '523ad47277ad11e7b5a5be2e44b06b34'::uuid
      WHEN 'GPS'  THEN '523ad60277ad11e7b5a5be2e44b06b34'::uuid
      WHEN 'LEVEL'  THEN '523ad79277ad11e7b5a5be2e44b06b34'::uuid
      ELSE null::uuid
    END AS ground_elevation_method_guid                                    ,
    WELLS.BACKFILL_DEPTH AS bkfill_above_srfc_seal_depth                   ,
    WELLS.BACKFILL_TYPE  AS backfill_above_surface_seal                    ,
    WELLS.SEALANT_MATERIAL AS sealant_material                             ,
    WELLS.STATUS_OF_WELL_CODE            AS status_of_well_code 	         ,
    WELLS.OBSERVATION_WELL_NUMBER	       AS observation_well_number        ,
    WELLS.MINISTRY_OBSERVATION_WELL_STAT AS ministry_observation_well_stat ,
    WELLS.WELL_LICENCE_GENERAL_STATUS    AS well_licence_general_status    ,
    CASE WELLS.ALTERNATIVE_SPECIFICATIONS_IND
       WHEN 'N' THEN false
       WHEN 'Y' THEN true
       ELSE null
    END AS alternative_specifications_ind                                  ,
    WELLS.CONSTRUCTION_START_DATE AT TIME ZONE 'GMT'                       ,
    WELLS.CONSTRUCTION_END_DATE AT TIME ZONE 'GMT'                         ,
    WELLS.ALTERATION_START_DATE AT TIME ZONE 'GMT'                         ,
    WELLS.ALTERATION_END_DATE AT TIME ZONE 'GMT'                           ,
    WELLS.CLOSURE_START_DATE AT TIME ZONE 'GMT'                            ,
    WELLS.CLOSURE_END_DATE AT TIME ZONE 'GMT'                              ,
    /*DRILLING_COMPANY.DRILLING_COMPANY_GUID                                 ,*/
    WELLS.FINAL_CASING_STICK_UP                                            ,
    WELLS.ARTESIAN_FLOW_VALUE                                              ,
    WELLS.ARTESIAN_PRESSURE                                                ,
    WELLS.BEDROCK_DEPTH                                                    ,
    WELLS.WHERE_PLATE_ATTACHED                                             ,
    WELLS.WHEN_CREATED AS when_created                                     ,
    coalesce(WELLS.WHEN_UPDATED,WELLS.WHEN_CREATED) as when_updated        ,
    WELLS.WHO_CREATED as who_created                                       ,
    coalesce(WELLS.WHO_UPDATED,WELLS.WHO_CREATED) as who_updated
  FROM WELLS.WELLS_WELLS WELLS LEFT OUTER JOIN WELLS.WELLS_OWNERS OWNER ON OWNER.OWNER_ID=WELLS.OWNER_ID
                                    /*JOIN GWELLS.DRILLING_COMPANY DRILLING_COMPANY ON WELLS.DRILLER_COMPANY_CODE=DRILLING_COMPANY.DRILLING_COMPANY_CODE*/
  WHERE WELLS.ACCEPTANCE_STATUS_CODE != 'REJECTED';

  raise notice 'Preparing ETL report ...';

  SELECT count(*) from xform_gwells_well into xform_rows;
  raise notice '... % rows loaded into the xform_gwells_well table', 	xform_rows;

  raise notice 'Finished populate_xform_gwells_well() procedure.';

END;
$$ LANGUAGE plpgsql;
