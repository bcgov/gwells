--  Run this script as gwells owner (e.g. psql -d gwells -U userGN0)
DROP FUNCTION IF EXISTS gwells_setup_replicate(); 
CREATE OR REPLACE FUNCTION gwells_setup_replicate() RETURNS void AS $$
BEGIN
	raise notice 'Starting gwells_setup_replicate() procedure...';	

	-- Reset tables
	raise notice '... clearing gwells.lithology_description data table';
	delete from gwells.lithology_description;
	raise notice '... clearing gwells.activity_submission data table';
	delete from gwells.activity_submission;
	raise notice '... clearing gwells.well data table';
	delete from gwells.well;

	raise notice '... clearing gwells.intended_water_use data table';		
	delete from gwells.intended_water_use;
	raise notice '... clearing gwells.well_subclass data table';
	delete from gwells.well_subclass;
	raise notice '... clearing gwells.well_class data table';
	delete from gwells.well_class;

	raise notice '... clearing gwells.province_state data table';
	delete from gwells.province_state;
	raise notice '... clearing gwells.well_yield_unit data table';
	delete from gwells.well_yield_unit;
	raise notice '... clearing gwells.drilling_method data table';
	delete from gwells.drilling_method;
	raise notice '... clearing gwells.ground_elevation_method data table';
	delete from gwells.ground_elevation_method;
	raise notice '... clearing gwells.land_district data table';
	delete from gwells.land_district;
	raise notice '... clearing gwells.well_status data table';
	delete from gwells.well_status;
	raise notice '... clearing gwells.licensed_status data table';
	delete from gwells.licensed_status;


	raise notice '... recreating xform_gwells_well ETL table';
	DROP TABLE IF EXISTS xform_gwells_well;
	CREATE unlogged TABLE IF NOT EXISTS xform_gwells_well (
	   well_tag_number              integer,
	   well_guid                    uuid,
	   acceptance_status_code       character varying(10),
	   owner_full_name              character varying(200),
	   owner_mailing_address        character varying(100),
	   owner_city                   character varying(100),
	   owner_postal_code            character varying(10),
	   street_address               character varying(100),
	   city                         character varying(50),
	   legal_lot                    character varying(10),
	   legal_plan                   character varying(20),
	   legal_district_lot           character varying(20),
	   legal_block                  character varying(10),
	   legal_section                character varying(10),
	   legal_township               character varying(20),
	   legal_range                  character varying(10),
	   legal_pid                    integer,
	   well_location_description    character varying(500),
	   identification_plate_number  integer,
	   diameter                     character varying(9),
	   total_depth_drilled          numeric(7,2),
	   finished_well_depth          numeric(7,2),
	   well_yield                   numeric(8,3),
	   WELL_USE_CODE                character varying(10),
	   LEGAL_LAND_DISTRICT_CODE     character varying(10),
	   province_state_guid          uuid,
	   CLASS_OF_WELL_CODCLASSIFIED_BY character varying(10),
	   SUBCLASS_OF_WELL_CLASSIFIED_BY character varying(10),
	   well_yield_unit_guid         uuid,
	   latitude                     numeric(8,6),
	   longitude                    numeric(9,6),
	   ground_elevation             numeric(10,2),   
	   orientation_vertical         boolean,
	   other_drilling_method  character varying(50),
	   drilling_method_guid         uuid,
	   ground_elevation_method_guid uuid,
	   BKFILL_ABOVE_SRFC_SEAL_DEPTH numeric(7,2), -- backfill_above_surface_seal_depth
	   backfill_above_surface_seal  character varying(250),
	   SEALANT_MATERIAL             character varying(100),
	   status_of_well_code 	          character varying(10),
	   observation_well_number	      integer,
	   ministry_observation_well_stat character varying(25),
	   well_licence_general_status    character varying(20),
	   alternative_specifications_ind boolean,
	   when_created                 timestamp with time zone,
	   when_updated                 timestamp with time zone,
	   who_created                  character varying(30),
	   who_updated                  character varying(30)    
	);

	-- Setup cron job.
	raise notice 'Finished gwells_setup_replicate() procedure.';	
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS gwells_replicate();
-- Must be run as PostgreSQL admin due to the 'copy' commands (i.e. psql -d gwells)
CREATE OR REPLACE FUNCTION gwells_replicate() RETURNS void AS $$
DECLARE
	wells_rows integer;
BEGIN
	raise notice 'Starting gwells_replicate() procedure...';	

	-- Get static code tables from GitHub
	raise notice '... importing gwells.intended_water_use code table';	
	copy gwells.intended_water_use (intended_water_use_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from program 'wget https://raw.githubusercontent.com/bcgov/gwells/master/database/code-tables/gwells_intended_water_use.csv -O - -q' header delimiter ',' CSV ; 
	raise notice '... importing gwells.well_class code table';	
	copy gwells.well_class (well_class_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from program 'wget https://raw.githubusercontent.com/bcgov/gwells/master/database/code-tables/gwells_well_class.csv -O - -q' header delimiter ',' CSV ; 
	raise notice '... importing gwells.well_subclass code table';	
	copy gwells.well_subclass (well_subclass_guid,code,description,is_hidden,sort_order,well_class_guid,when_created,when_updated,who_created,who_updated) from program 'wget https://raw.githubusercontent.com/bcgov/gwells/master/database/code-tables/gwells_well_subclass.csv -O - -q' header delimiter ',' CSV ; 
	raise notice '... importing gwells.province_state code table';	
	copy gwells.province_state (province_state_guid,code,description,sort_order,when_created,when_updated,who_created,who_updated) from program 'wget https://raw.githubusercontent.com/bcgov/gwells/master/database/code-tables/gwells_province_state.csv -O - -q' header delimiter ',' CSV ; 
	raise notice '... importing gwells.well_yield_unit code table';	
	copy gwells.well_yield_unit (well_yield_unit_guid,code,description,sort_order,when_created,when_updated,who_created,who_updated) from program 'wget https://raw.githubusercontent.com/bcgov/gwells/master/database/code-tables/gwells_well_yield_unit.csv -O - -q' header delimiter ',' CSV ; 
	raise notice '... importing gwells.drilling_method code table';	
	copy gwells.drilling_method (drilling_method_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from program 'wget https://raw.githubusercontent.com/bcgov/gwells/master/database/code-tables/gwells_drilling_method.csv -O - -q' header delimiter ',' CSV ; 
	raise notice '... importing gwells.ground_elevation_method code table';	
	copy gwells.ground_elevation_method (ground_elevation_method_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from program 'wget https://raw.githubusercontent.com/bcgov/gwells/master/database/code-tables/gwells_ground_elevation_method.csv -O - -q' header delimiter ',' CSV ; 
	raise notice '... importing gwells.well_status code table';	
	copy gwells.well_status (well_status_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from program 'wget https://raw.githubusercontent.com/bcgov/gwells/master/database/code-tables/gwells_well_status.csv -O - -q' header delimiter ',' CSV ; 
	raise notice '... importing gwells.licensed_status code table';	
	copy gwells.licensed_status (well_licensed_status_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from program 'wget https://raw.githubusercontent.com/bcgov/gwells/master/database/code-tables/gwells_licensed_status.csv -O - -q' header delimiter ',' CSV ; 

	raise notice '... importing gwells.land_district data table';	
	INSERT INTO gwells.land_district (
		land_district_guid,code,name,sort_order,when_created,when_updated,who_created,who_updated) 
	SELECT 
		gen_random_uuid(),LEGAL_LAND_DISTRICT_CODE,LEGAL_LAND_DISTRICT_NAME,SORT_ORDER,WHEN_CREATED,
		coalesce(WHEN_UPDATED,WHEN_CREATED),WHO_CREATED ,coalesce(WHO_UPDATED,WHO_CREATED) -- STATUS_FLAG
	FROM WELLS.LEGAL_LAND_DIST_CODES
	ORDER BY LEGAL_LAND_DISTRICT_CODE ASC;

	raise notice '... transforming wells data (!= REJECTED) via xform_gwells_well ETL table...';	
	INSERT INTO xform_gwells_well (
		well_tag_number                ,
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
		well_yield                     ,
		well_use_code                  ,
		legal_land_district_code       ,
		province_state_guid            ,
		class_of_well_codclassified_by ,
		subclass_of_well_classified_by ,
		well_yield_unit_guid           ,
		latitude                       ,
		longitude                      ,
		ground_elevation               ,
		orientation_vertical           ,
		other_drilling_method          ,
		drilling_method_guid           ,
		ground_elevation_method_guid   ,
		bkfill_above_srfc_seal_depth   ,
		backfill_above_surface_seal    ,
		sealant_material               ,
 	    	status_of_well_code           ,
	    	observation_well_number	      ,
	    	ministry_observation_well_stat,
	    	well_licence_general_status   ,
	    	alternative_specifications_ind,
		when_created                   ,
		when_updated                   ,
		who_created                    ,
		who_updated)
	SELECT
	  WELLS.WELL_TAG_NUMBER,
	  null, -- gen_random_uuid()  AS WELL_GUID, 
	  WELLS.ACCEPTANCE_STATUS_CODE AS acceptance_status_code,
	  concat_ws(' ', owner.giVEN_NAME,OWNER.SURNAME) AS owner_full_name,
	  concat_ws(' ',OWNER.STREET_NUMBER,STREET_NAME) AS owner_mailing_address,  
	  OWNER.CITY AS owner_city,
	  OWNER.POSTAL_CODE AS owner_postal_code,
	  WELLS.SITE_STREET AS street_address,
	  WELLS.SITE_AREA AS city,
	  WELLS.LOT_NUMBER AS legal_lot,
	  WELLS.LEGAL_PLAN AS legal_plan,
	  WELLS.LEGAL_DISTRICT_LOT AS legal_district_lot,
	  WELLS.LEGAL_BLOCK AS legal_block,
	  WELLS.LEGAL_SECTION AS legal_section,
	  WELLS.LEGAL_TOWNSHIP AS legal_township,
	  WELLS.LEGAL_RANGE AS legal_range,
	  WELLS.PID AS legal_pid,
	  WELLS.WELL_LOCATION AS well_location_description,
	  WELLS.WELL_IDENTIFICATION_PLATE_NO AS identification_plate_number,
	  WELLS.DIAMETER AS diameter,
	  WELLS.TOTAL_DEPTH_DRILLED AS total_depth_drilled,
	  WELLS.DEPTH_WELL_DRILLED AS finished_well_depth,
	  WELLS.YIELD_VALUE AS well_yield,
	  WELLS.WELL_USE_CODE, -- -> intended_water_use_guid
	  WELLS.LEGAL_LAND_DISTRICT_CODE, -- -> legal_land_district_guid
	  CASE OWNER.PROVINCE_STATE_CODE
	    WHEN 'BC' THEN 'f46b70b647d411e7a91992ebcb67fe33'::uuid
	    WHEN 'AB' THEN 'f46b742647d411e7a91992ebcb67fe33'::uuid
	    WHEN 'WASH_STATE' THEN 'f46b77b447d411e7a91992ebcb67fe33'::uuid
	    ELSE 'f46b7b1a47d411e7a91992ebcb67fe33'::uuid
	  END AS province_state_guid,
	  coalesce (WELLS.CLASS_OF_WELL_CODCLASSIFIED_BY,'LEGACY'),
	  WELLS.SUBCLASS_OF_WELL_CLASSIFIED_BY, -- -> well_subclass_guid
	  CASE WELLS.YIELD_UNIT_CODE 
	    WHEN 'GPM'  THEN 'c4634ef447c311e7a91992ebcb67fe33'::uuid
	    WHEN 'IGM'  THEN 'c4634ff847c311e7a91992ebcb67fe33'::uuid
	    WHEN 'DRY'  THEN 'c46347b047c311e7a91992ebcb67fe33'::uuid
	    WHEN 'LPS'  THEN 'c46350c047c311e7a91992ebcb67fe33'::uuid
	    WHEN 'USGM' THEN 'c463525047c311e7a91992ebcb67fe33'::uuid
	    WHEN 'GPH'  THEN 'c4634b4847c311e7a91992ebcb67fe33'::uuid
	    WHEN 'UNK'  THEN 'c463518847c311e7a91992ebcb67fe33'::uuid
	    ELSE 'c463518847c311e7a91992ebcb67fe33'::uuid -- As PostGres didn't like "" as guid value 
	  END AS well_yield_unit_guid,
	  WELLS.LATITUDE,
	  CASE
	    WHEN WELLS.LONGITUDE > 0 THEN WELLS.LONGITUDE * -1
	    ELSE WELLS.LONGITUDE 
	  END AS longitude,  
	  WELLS.ELEVATION AS ground_elevation,
	  CASE WELLS.ORIENTATION_OF_WELL_CODE 
	     WHEN 'HORIZ' THEN false
	     ELSE true
	  END AS orientation_vertical,
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
	  END AS drilling_method_guid,
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
	  END AS ground_elevation_method_guid,
	  WELLS.BACKFILL_DEPTH AS bkfill_above_srfc_seal_depth,
	  WELLS.BACKFILL_TYPE  AS backfill_above_surface_seal,
	  WELLS.SEALANT_MATERIAL AS sealant_material,
	  WELLS.STATUS_OF_WELL_CODE            AS status_of_well_code 	        ,
	  WELLS.OBSERVATION_WELL_NUMBER	       AS observation_well_number       ,
	  WELLS.MINISTRY_OBSERVATION_WELL_STAT AS ministry_observation_well_stat,
	  WELLS.WELL_LICENCE_GENERAL_STATUS    AS well_licence_general_status   ,
	  CASE WELLS.ALTERNATIVE_SPECIFICATIONS_IND  
	     WHEN 'N' THEN false
	     WHEN 'Y' THEN true
	     ELSE null
	  END AS alternative_specifications_ind,
	  WELLS.WHEN_CREATED AS when_created,
	  coalesce(WELLS.WHEN_UPDATED,WELLS.WHEN_CREATED) as when_updated,
	  WELLS.WHO_CREATED as who_created,
	  coalesce(WELLS.WHO_UPDATED,WELLS.WHO_CREATED) as who_updated
	FROM WELLS.WELLS WELLS LEFT OUTER JOIN WELLS.OWNERS OWNER
	  ON OWNER.OWNER_ID=WELLS.OWNER_ID
	WHERE WELLS.ACCEPTANCE_STATUS_CODE != 'REJECTED';

	raise notice '... importing ETL into the main "wells" table';	
	INSERT INTO gwells.well (
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
	  legal_pid                   ,
	  well_location_description   ,
	  identification_plate_number ,
	  diameter                    ,
	  total_depth_drilled         ,
	  finished_well_depth         ,
	  well_yield                  ,
	  intended_water_use_guid     ,
	  legal_land_district_guid    ,
	  province_state_guid         ,
	  well_class_guid             ,
	  well_subclass_guid          ,
	  well_yield_unit_guid        ,
	  latitude,
	  longitude,
	  ground_elevation,
	  orientation_vertical,
	  other_drilling_method,
	  drilling_method_guid,
	  ground_elevation_method_guid,
	  when_created                ,
	  when_updated                ,
	  who_created                 ,
	  who_updated                 ,
	  backfill_above_surface_seal_depth,
	  surface_seal_depth        ,
	  surface_seal_thickness    ,
	  surface_seal_method_guid  ,
	  backfill_above_surface_seal,
	 well_status_guid,
	 licensed_status_guid,
	  surface_seal_material_guid,
	  other_screen_bottom         ,  
	  other_screen_material       ,   
	  development_notes,
	  where_plate_attached,
	  water_quality_colour     , 
	  water_quality_odour      , 
	  well_cap_type            , 
	  well_disinfected         , 
	  alternative_specs_submitted,
	  comments                   
	  )
	SELECT 
		xform.well_tag_number              ,
		gen_random_uuid()                 ,
		coalesce(xform.owner_full_name,' '),
		coalesce(xform.owner_mailing_address, ' '),
		coalesce(xform.owner_city, ' '),
		coalesce(xform.owner_postal_code , ' '),
		coalesce(xform.street_address    , ' '),
		coalesce(xform.city              , ' '),
		coalesce(xform.legal_lot         , ' '),
		coalesce(xform.legal_plan        , ' '),
		coalesce(xform.legal_district_lot, ' '),
		coalesce(xform.legal_block       , ' '),
		coalesce(xform.legal_section     , ' '),
		coalesce(xform.legal_township    , ' '),
		coalesce(xform.legal_range       , ' '),
		xform.legal_pid,
		coalesce(xform.well_location_description,' '),
		xform.identification_plate_number  ,
		coalesce(xform.diameter, ' '),
		xform.total_depth_drilled          ,
		xform.finished_well_depth          ,
		xform.well_yield                   ,
		use.intended_water_use_guid      ,
		land.land_district_guid          ,
		xform.province_state_guid          ,
		class.well_class_guid     ,
		subclass.well_subclass_guid   ,
		xform.well_yield_unit_guid      ,
		xform.latitude                  ,
		xform.longitude                 ,
		xform.ground_elevation,
		xform.orientation_vertical      ,
		' ',
		xform.drilling_method_guid ,
		xform.ground_elevation_method_guid,
		xform.when_created              ,
		xform.when_updated,
		xform.who_created               ,
		xform.who_updated      ,
		xform.bkfill_above_srfc_seal_depth,
		null,
		null,
		null,
		coalesce(xform.backfill_above_surface_seal,' '),
		well_status.well_status_guid,
		licenced_status.well_licensed_status_guid,
		null,
		'',
		'',
		'',
		'',
		'',
		'',
		'',
		false,
		false,
		''
	FROM xform_gwells_well xform
	LEFT OUTER JOIN gwells.intended_water_use use ON xform.WELL_USE_CODE=use.code
	LEFT OUTER JOIN gwells.well_status well_status ON xform.STATUS_OF_WELL_CODE=upper(well_status.code)
	LEFT OUTER JOIN gwells.licensed_status licenced_status ON xform.WELL_LICENCE_GENERAL_STATUS=upper(licenced_status.code)
	LEFT OUTER JOIN gwells.land_district     land ON xform.LEGAL_LAND_DISTRICT_CODE=land.code 
	INNER      JOIN gwells.well_class       class ON xform.CLASS_OF_WELL_CODCLASSIFIED_BY=class.code 
	LEFT OUTER JOIN gwells.well_subclass subclass ON xform.SUBCLASS_OF_WELL_CLASSIFIED_BY=subclass.code 
	AND subclass.well_class_guid = class.well_class_guid ;

	select count(*) from gwells.well into wells_rows;
	raise notice '... % rows loaded into the main "wells" table', 	wells_rows;	
	raise notice 'Finished gwells_replicate() procedure.';	
END;
$$ LANGUAGE plpgsql;
