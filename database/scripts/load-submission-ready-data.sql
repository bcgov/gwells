\encoding windows-1251
\copy gwells_well_yield_unit 	  FROM './gwells_well_yield_unit.csv'   HEADER DELIMITER ',' CSV
\copy gwells_province_state  	  FROM './gwells_province_state.csv' 	   HEADER DELIMITER ',' CSV
\copy gwells_well_activity_type (well_activity_type_guid,code,description,is_hidden,sort_order,who_created,when_created,who_updated,when_updated) FROM './gwells_well_activity_type.csv' HEADER DELIMITER ',' CSV

\copy gwells_intended_water_use	FROM './gwells_intended_water_use.csv' HEADER DELIMITER ',' CSV
\copy gwells_well_class  	    	FROM './gwells_well_class.csv'  	   	HEADER DELIMITER ',' CSV
\copy gwells_well_subclass    	FROM './gwells_well_subclass.csv'     HEADER DELIMITER ',' CSV
\copy gwells_drilling_method    FROM './gwells_drilling_method.csv'    HEADER DELIMITER ',' CSV
\copy gwells_ground_elevation_method FROM './gwells_ground_elevation_method.csv' HEADER DELIMITER ',' CSV
\copy gwells_lithology_structure FROM './gwells_lithology_structure.csv' HEADER DELIMITER ',' CSV
\copy gwells_lithology_moisture  FROM './gwells_lithology_moisture.csv'  HEADER DELIMITER ',' CSV
\copy gwells_lithology_hardness  FROM './gwells_lithology_hardness.csv'  HEADER DELIMITER ',' CSV
\copy gwells_bedrock_material_descriptor FROM './gwells_bedrock_material_descriptor.csv' HEADER DELIMITER ',' CSV
\copy gwells_bedrock_material     FROM './gwells_bedrock_material.csv' HEADER DELIMITER ',' CSV
\copy gwells_lithology_colour     FROM './gwells_lithology_colour.csv' HEADER DELIMITER ',' CSV
\copy gwells_surficial_material   FROM './gwells_surficial_material.csv'   HEADER DELIMITER ',' CSV

\copy gwells_casing_material FROM './gwells_casing_material.csv' HEADER DELIMITER ',' CSV
\copy gwells_casing_type     FROM './gwells_casing_type.csv'     HEADER DELIMITER ',' CSV

\copy gwells_screen_type     FROM './gwells_screen_type.csv'     HEADER DELIMITER ',' CSV
\copy gwells_screen_intake   FROM './gwells_screen_intake.csv'   HEADER DELIMITER ',' CSV
\copy gwells_screen_opening  FROM './gwells_screen_opening.csv'  HEADER DELIMITER ',' CSV
\copy gwells_screen_bottom   FROM './gwells_screen_bottom.csv'   HEADER DELIMITER ',' CSV
\copy gwells_screen_material FROM './gwells_screen_material.csv' HEADER DELIMITER ',' CSV
\copy gwells_liner_material FROM './gwells_liner_material.csv' HEADER DELIMITER ',' CSV
\copy gwells_filter_pack_material FROM './gwells_filter_pack_material.csv' HEADER DELIMITER ',' CSV
\copy gwells_filter_pack_material_size FROM './gwells_filter_pack_material_size.csv' HEADER DELIMITER ',' CSV

\copy gwells_screen_assembly_type    FROM './gwells_screen_assembly_type.csv'    HEADER DELIMITER ',' CSV 
\copy gwells_development_method      FROM './gwells_development_method.csv'      HEADER DELIMITER ',' CSV
\copy gwells_yield_estimation_method FROM './gwells_yield_estimation_method.csv' HEADER DELIMITER ',' CSV

/* This will need further transformation to link to existing data */
CREATE unlogged TABLE IF NOT EXISTS xform_gwells_surface_seal_method (
  who_created              character varying(30)   ,
  when_created             timestamp with time zone,
  who_updated              character varying(30)   ,
  when_updated             timestamp with time zone,
  surface_seal_method_guid uuid                    ,
  code                     character varying(10)   ,
  description              character varying(100)  ,
  is_hidden                boolean                 ,
  sort_order               integer                 
);

/* This will need further transformation to link to existing data */
CREATE unlogged TABLE IF NOT EXISTS xform_gwells_surface_seal_material (
  who_created                 character varying(30)   ,
  when_created                timestamp with time zone,
  who_updated                 character varying(30)   ,
  when_updated                timestamp with time zone,
  surface_seal_material_guid  uuid                    ,
  code                        character varying(100)   ,
  description                 character varying(100)  ,
  is_hidden                   boolean                 ,
  sort_order                  integer       ,
  SEALANT_MATERIAL            character varying(100)          
);
/* - make distinct on CODE */ 

CREATE unlogged TABLE IF NOT EXISTS xform_gwells_land_district (
  land_district_guid uuid,
  code               character varying(10),
  name               character varying(255),
  sort_order         integer,
  when_created       timestamp with time zone,
  when_updated       timestamp with time zone,
  who_created        character varying(30)   ,
  who_updated        character varying(30) 
);

CREATE unlogged TABLE IF NOT EXISTS xform_gwells_well (
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
   latitude                     numeric(8,6)             ,
   longitude                    numeric(9,6)             ,
   ground_elevation             numeric(10,2) ,   
   orientation_vertical         boolean,
   other_drilling_method  character varying(50)   ,
   drilling_method_guid         uuid   ,
   ground_elevation_method_guid uuid ,
   BKFILL_ABOVE_SRFC_SEAL_DEPTH numeric(7,2), /* backfill_above_surface_seal_depth */
   backfill_above_surface_seal  character varying(250),
   SEALANT_MATERIAL             character varying(100) ,
   when_created                 timestamp with time zone,
   when_updated                 timestamp with time zone,
   who_created                  character varying(30)   ,
   who_updated                  character varying(30)    
);

CREATE unlogged TABLE IF NOT EXISTS xform_gwells_drilling_company (
 drilling_company_guid uuid                   ,
 name                  character varying(200) ,
 is_hidden             boolean,
 when_created          timestamp with time zone,
 when_updated          timestamp with time zone,
 who_created           character varying(30)   ,
 who_updated           character varying(30)   ,  
 DRILLER_COMPANY_CODE  character varying(30)             
);

CREATE unlogged TABLE IF NOT EXISTS xform_gwells_driller (
  driller_guid          uuid                   ,
  first_name            character varying(100) ,
  surname               character varying(100) ,
  registration_number   character varying(100) ,
  is_hidden             boolean                ,
  when_created          timestamp with time zone,
  when_updated          timestamp with time zone,
  who_created           character varying(30)   ,
  who_updated           character varying(30)   ,    
  DRILLER_COMPANY_CODE  character varying(30)            
);


\encoding windows-1251
\copy xform_gwells_land_district    FROM './xform_gwells_land_district.csv'    HEADER DELIMITER ',' CSV
\copy xform_gwells_drilling_company FROM './xform_gwells_drilling_company.csv' HEADER DELIMITER ',' CSV
\copy xform_gwells_driller          FROM './xform_gwells_driller.csv'          HEADER DELIMITER ',' CSV
\copy xform_gwells_well             FROM './xform_gwells_well.csv'  WITH (HEADER, DELIMITER ',' , FORMAT CSV, FORCE_NULL(when_updated,drilling_method_guid,ground_elevation_method_guid));

\copy xform_gwells_surface_seal_material FROM './xform_gwells_surface_seal_material.csv' HEADER DELIMITER ',' CSV
\copy xform_gwells_surface_seal_method FROM './xform_gwells_surface_seal_method.csv' HEADER DELIMITER ',' CSV


INSERT INTO gwells_surface_seal_material (who_created,when_created,who_updated,when_updated,
    surface_seal_material_guid,code,description,is_hidden,sort_order)
SELECT who_created,when_created,who_updated,when_updated,
  surface_seal_material_guid, code,description,is_hidden,sort_order
FROM xform_gwells_surface_seal_material
WHERE length(code) < 11
AND  code not in 
  (SELECT CODE
  FROM xform_gwells_surface_seal_material
  group by code
  having count(*) > 1);

INSERT INTO gwells_surface_seal_method (who_created,when_created,who_updated,when_updated,
    surface_seal_method_guid,code,description,is_hidden,sort_order)
SELECT who_created,when_created,who_updated,when_updated,
  surface_seal_method_guid, code,description,is_hidden,sort_order
FROM xform_gwells_surface_seal_method;


INSERT INTO gwells_land_district (land_district_guid, code, name, sort_order,
  when_created, when_updated, who_created, who_updated)
SELECT land_district_guid, code, name, sort_order,when_created, when_updated, who_created, who_updated
FROM xform_gwells_land_district;

INSERT INTO gwells_drilling_company (drilling_company_guid, name, is_hidden,
   when_created, when_updated, who_created , who_updated /* , driller_company_code */)
SELECT drilling_company_guid, name, is_hidden,
  when_created, when_updated, who_created , who_updated /* driller_company_code */
FROM xform_gwells_drilling_company;

INSERT INTO GWELLS_DRILLING_COMPANY (drilling_company_guid, name, is_hidden,
   when_created, when_updated, who_created , who_updated /* , driller_company_code */)
VALUES ('018d4c1047cb11e7a91992ebcb67fe33',
        'Data Conversion Drilling Compnay',
        true,
        '2017-07-01 00:00:00-08',
        '2017-07-01 00:00:00-08',  
        'ETL_USER',
        'ETL_USER'
);

INSERT INTO gwells_driller (driller_guid, first_name, surname, registration_number, is_hidden, drilling_company_guid,
  when_created, when_updated, who_created, who_updated)
SELECT dr.driller_guid, dr.first_name, dr.surname, dr.registration_number, dr.is_hidden, 
co.drilling_company_guid, dr.when_created, dr.when_updated, dr.who_created, dr.who_updated
FROM  xform_gwells_driller dr, xform_gwells_drilling_company co
WHERE dr.DRILLER_COMPANY_CODE = co.DRILLER_COMPANY_CODE;

INSERT INTO gwells_well (
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
  surface_seal_material_guid,
  /*  
  liner_diameter             ,  
  liner_from                 ,  
  liner_thickness            ,  
  liner_to                   ,  
  liner_material_guid        ,  
  filter_pack_from           ,  
  filter_pack_thickness      ,  
  filter_pack_to             ,  
  */
  other_screen_bottom         ,  
  other_screen_material       ,   
  /*
  filter_pack_material_guid   ,    
  filter_pack_material_size_guid,  
  screen_bottom_guid  ,            
  screen_intake_guid  ,            
  screen_opening_guid ,           
  screen_type_guid    ,
  development_hours   ,
  */    
  development_notes,
  /*
  development_notes,
  */
  where_plate_attached,
  /*
  screen_material_guid     , 
  */
  water_quality_colour     , 
  water_quality_odour      , 
  /*
  artestian_flow           , 
  artestian_pressure       , 
  bedrock_depth            , 
  final_casing_stick_up    , 
  static_water_level       , 
  */
  well_cap_type            , 
  well_disinfected         , 
  alternative_specs_submitted,
  comments                   
  )
SELECT 
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
old.GROUND_ELEVATION,
old.orientation_vertical      ,
old.other_drilling_method,
old.drilling_method_guid ,
old.ground_elevation_method_guid,
old.when_created              ,
coalesce(old.when_updated,old.when_created),
old.who_created               ,
old.who_updated      ,
old.bkfill_above_srfc_seal_depth,
null,
null,
null,
old.backfill_above_surface_seal,
null, /* seal_material.surface_seal_material_guid   Should match  INSERT 0 111556 */
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
FROM xform_gwells_well old
LEFT OUTER JOIN gwells_intended_water_use  use   ON old.WELL_USE_CODE  = use.code
LEFT OUTER JOIN xform_gwells_land_district land  ON old.LEGAL_LAND_DISTRICT_CODE = land.code 
INNER      JOIN gwells_well_class          class ON old.CLASS_OF_WELL_CODCLASSIFIED_BY = class.code 
LEFT OUTER JOIN gwells_well_subclass   subclass  ON old.SUBCLASS_OF_WELL_CLASSIFIED_BY = subclass.code 
                AND subclass.well_class_guid = class.well_class_guid
/*
LEFT OUTER JOIN xform_gwells_surface_seal_material seal_material 
  ON old.SEALANT_MATERIAL = seal_material.SEALANT_MATERIAL 
*/
;