\encoding windows-1251
\copy gwells_well_yield_unit 	  FROM './gwells_well_yield_unit.csv' 	  HEADER DELIMITER ',' CSV
\copy gwells_province_state  	  FROM './gwells_province_state.csv' 	  HEADER DELIMITER ',' CSV
\copy gwells_well_activity_type FROM './gwells_well_activity_type.csv' HEADER DELIMITER ',' CSV
\copy gwells_intended_water_use	FROM './gwells_intended_water_use.csv' HEADER DELIMITER ',' CSV
\copy gwells_well_class  	    	FROM './gwells_well_class.csv'  	    	HEADER DELIMITER ',' CSV
\copy gwells_well_subclass    	FROM './gwells_well_subclass.csv'   	  HEADER DELIMITER ',' CSV
\copy gwells_drilling_method    FROM './gwells_drilling_method.csv'    HEADER DELIMITER ',' CSV
\copy gwells_ground_elevation_method FROM './gwells_ground_elevation_method.csv' HEADER DELIMITER ',' CSV

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
   CLASS_OF_WELL_CODCLASSIFIED_BY character varying(10)  ,
   SUBCLASS_OF_WELL_CLASSIFIED_BY character varying(10)  ,
   well_yield_unit_guid         uuid                     ,
   DRILLING_METHOD_CODE         character varying(10)    ,
   LATITUDE                     numeric(8,6)             ,
   LONGITUDE                    numeric(9,6)             ,
   UTM_NORTH                    integer,
   UTM_EAST                     integer,
   UTM_ZONE_CODE                character varying(10)  ,
   ORIENTATION_VERTICAL         boolean
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
\copy xform_gwells_land_district    FROM './xform_gwells_land_district.csv'    HEADER DELIMITER ',' CSV
\copy xform_gwells_drilling_company FROM './xform_gwells_drilling_company.csv' HEADER DELIMITER ',' CSV
\copy xform_gwells_driller          FROM './xform_gwells_driller.csv'          HEADER DELIMITER ',' CSV
\copy xform_gwells_well             FROM './xform_gwells_well.csv'  WITH (HEADER, DELIMITER ',' , FORMAT CSV, FORCE_NULL(modified));


INSERT INTO gwells_land_district (land_district_guid, code, name, sort_order)   
SELECT land_district_guid, code, name, sort_order
FROM xform_gwells_land_district;

INSERT INTO gwells_drilling_company (drilling_company_guid, name, is_hidden)
SELECT drilling_company_guid, name, is_hidden
FROM xform_gwells_drilling_company;

insert into gwells_drilling_company 
values ('018d4c1047cb11e7a91992ebcb67fe33',
        'Data Conversion Drilling Compnay',
        true
        );

/* Fri 23 Jun 14:49:59 2017 GW Distinct for now until data cleanup */

INSERT INTO gwells_driller (driller_guid, first_name, surname, registration_number, is_hidden, drilling_company_guid)
SELECT distinct driller.driller_guid, driller.first_name, driller.surname, driller.registration_number, driller.is_hidden, co.drilling_company_guid
FROM  xform_gwells_driller driller, xform_gwells_drilling_company co
WHERE driller.DRILLER_COMPANY_CODE = co.DRILLER_COMPANY_CODE;

/* TODO mismtach of counts 
INSERT INTO gwells_driller (driller_guid, first_name, surname, registration_number, is_hidden, drilling_company_guid)
SELECT driller.driller_guid, driller.first_name, driller.surname, driller.registration_number, driller.is_hidden, '018d4c1047cb11e7a91992ebcb67fe33'
FROM  xform_gwells_driller driller
WHERE driller.DRILLER_COMPANY_CODE is null;
*/

INSERT INTO gwells_well (
  created                     ,
  modified                    ,
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
  orientation_vertical 
  )
SELECT 
old.created                      ,
coalesce(old.modified,old.created),
old.well_tag_number              ,
old.well_guid                    ,
old.owner_full_name              ,
old.owner_mailing_address        ,
old.owner_city                   ,
old.owner_postal_code            ,
old.street_address               ,
old.city                         ,
old.legal_lot                    ,
old.legal_plan                   ,
old.legal_district_lot           ,
old.legal_block                  ,
old.legal_section                ,
old.legal_township               ,
old.legal_range                  ,
old.legal_pid                    ,
old.well_location_description    ,
old.identification_plate_number  ,
old.diameter                     ,
old.total_depth_drilled          ,
old.finished_well_depth          ,
old.well_yield                   ,
use.intended_water_use_guid      ,
land.land_district_guid          ,
old.province_state_guid          ,
class.well_class_guid     ,
subclass.well_subclass_guid   ,
old.well_yield_unit_guid      ,
old.LATITUDE                  ,
old.LONGITUDE                 ,
old.orientation_vertical
FROM xform_gwells_well old
LEFT OUTER JOIN gwells_intended_water_use  use   ON old.WELL_USE_CODE  = use.code
LEFT OUTER JOIN xform_gwells_land_district land  ON old.LEGAL_LAND_DISTRICT_CODE = land.code 
INNER      JOIN gwells_well_class          class ON old.CLASS_OF_WELL_CODCLASSIFIED_BY = class.code 
LEFT OUTER JOIN gwells_well_subclass   subclass  ON old.SUBCLASS_OF_WELL_CLASSIFIED_BY = subclass.code 
                AND subclass.well_class_guid = class.well_class_guid;