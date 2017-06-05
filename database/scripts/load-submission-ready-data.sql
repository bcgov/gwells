\encoding windows-1251
\copy gwells_well_yield_unit 	  FROM './postgres/gwells_well_yield_unit.csv' 	  HEADER DELIMITER ',' CSV
\copy gwells_province_state  	  FROM './postgres/gwells_province_state.csv' 	  HEADER DELIMITER ',' CSV
\copy gwells_well_activity_type FROM './postgres/gwells_well_activity_type.csv' HEADER DELIMITER ',' CSV
\copy gwells_intended_water_use	FROM './postgres/gwells_intended_water_use.csv' HEADER DELIMITER ',' CSV
\copy gwells_well_class  	    	FROM './postgres/gwells_well_class.csv'  	    	HEADER DELIMITER ',' CSV
\copy gwells_well_subclass    	FROM './postgres/gwells_well_subclass.csv'   	  HEADER DELIMITER ',' CSV

CREATE unlogged TABLE IF NOT EXISTS xform_gwells_land_district (
  land_district_guid uuid,
  code               character varying(10),
  name               character varying(255),
  sort_order         integer
);

CREATE unlogged TABLE IF NOT EXISTS xform_gwells_well (
   created                      timestamp with time zone ,
   modified                     timestamp with time zone ,
   well_tag_number              integer                  ,
   well_guid                    uuid                     ,
   owner_full_name              character varying(200)   ,
   owner_mailing_address        character varying(100)   ,
   owner_city                   character varying(100)   ,
   owner_postal_code            character varying(10)    ,
   street_address               character varying(100)   ,
   city                         character varying(50)    ,
   legal_lot                    character varying(10)    ,
   legal_plan                   character varying(20)    ,
   legal_district_lot           character varying(20)    ,
   legal_block                  character varying(10)    ,
   legal_section                character varying(10)    ,
   legal_township               character varying(20)    ,
   legal_range                  character varying(10)    ,
   legal_pid                    integer                  ,
   well_location_description    character varying(500)   ,
   identification_plate_number  integer                  ,
   diameter                     character varying(9)     ,
   total_depth_drilled          numeric(7,2)             ,
   finished_well_depth          numeric(7,2)             ,
   well_yield                   numeric(8,3)             ,
   WELL_USE_CODE                character varying(10)    ,
   LEGAL_LAND_DISTRICT_CODE     character varying(10)    ,
   province_state_guid          uuid                     ,
   CLASS_OF_WELL_CODE           character varying(30)    ,
   SUBCLASS_OF_WELL_CODE        character varying(10)    ,
   well_yield_unit_guid         uuid                     ,
   LATITUDE                     numeric(8,6)             ,
   LONGITUDE                    numeric(9,6)             ,
   UTM_NORTH                    integer,
   UTM_EAST                     integer,
   UTM_ZONE_CODE                character varying(10)  
);


CREATE unlogged TABLE IF NOT EXISTS xform_gwells_drilling_company (
 drilling_company_guid uuid                   ,
 name                  character varying(200) ,
 is_hidden             boolean,
 DRILLER_COMPANY_CODE  character varying(30)             
);

CREATE unlogged TABLE IF NOT EXISTS xform_gwells_driller (
  driller_guid          uuid                   ,
  first_name            character varying(100) ,
  surname               character varying(100) ,
  registration_number   character varying(100) ,
  is_hidden             boolean                ,
 DRILLER_COMPANY_CODE  character varying(30)            
);

\encoding windows-1251
\copy xform_gwells_land_district    FROM './postgres/xform_gwells_land_district.csv'    HEADER DELIMITER ',' CSV
\copy xform_gwells_well             FROM './postgres/xform_gwells_well.csv'             HEADER DELIMITER ',' CSV
\copy xform_gwells_drilling_company FROM './postgres/xform_gwells_drilling_company.csv' HEADER DELIMITER ',' CSV
\copy xform_gwells_driller          FROM './postgres/xform_gwells_driller.csv'          HEADER DELIMITER ',' CSV

/*
insert into gwells_drilling_company 
values ('Data Conversion Drilling Compnay',
        true,
        '018d4c1047cb11e7a91992ebcb67fe33'
        )
;
*/


/* AND THEN INSERT INTO AS SELECT FROM... joined on FK */




