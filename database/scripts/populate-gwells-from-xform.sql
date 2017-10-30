DROP FUNCTION IF EXISTS populate_gwells_from_xform();

CREATE OR REPLACE FUNCTION populate_gwells_from_xform() RETURNS void AS $$

DECLARE

wells_rows integer;

BEGIN
  raise notice 'Starting populate_gwells_from_xform procedure...';
	raise notice '... importing ETL into the gwells_well table';
	INSERT INTO gwells_well (
	  well_tag_number                  ,
	  well_guid                        ,
	  owner_full_name                  ,
	  owner_mailing_address            ,
	  owner_city                       ,
	  owner_postal_code                ,
	  street_address                   ,
	  city                             ,
	  legal_lot                        ,
	  legal_plan                       ,
	  legal_district_lot               ,
	  legal_block                      ,
	  legal_section                    ,
	  legal_township                   ,
	  legal_range                      ,
	  legal_pid                        ,
	  well_location_description        ,
	  identification_plate_number      ,
	  diameter                         ,
	  total_depth_drilled              ,
	  finished_well_depth              ,
	  well_yield                       ,
	  intended_water_use_guid          ,
	  legal_land_district_guid         ,
	  province_state_guid              ,
	  well_class_guid                  ,
	  well_subclass_guid               ,
	  well_yield_unit_guid             ,
	  latitude                         ,
	  longitude                        ,
	  ground_elevation                 ,
	  well_orientation                 ,
	  other_drilling_method            ,
	  drilling_method_guid             ,
	  ground_elevation_method_guid     ,
	  when_created                     ,
	  when_updated                     ,
	  who_created                      ,
	  who_updated                      ,
	  backfill_above_surface_seal_depth,
	  surface_seal_depth               ,
	  surface_seal_thickness           ,
	  surface_seal_method_guid         ,
	  backfill_above_surface_seal      ,
	  well_status_guid                 ,
	  licensed_status_guid             ,
	  surface_seal_material_guid       ,
	  other_screen_bottom              ,
	  other_screen_material            ,
	  development_notes                ,
	  where_plate_attached             ,
	  water_quality_colour             ,
	  water_quality_odour              ,
	  well_cap_type                    ,
	  well_disinfected                 ,
	  alternative_specs_submitted      ,
	  comments                         ,
	  construction_start_date          ,
	  construction_end_date            ,
	  alteration_start_date            ,
	  alteration_end_date              ,
	  decommission_start_date          ,
	  decommission_end_date            ,
	  /*drilling_company_guid*/
    final_casing_stick_up            ,
    artesian_flow
	  )
	SELECT
		xform.well_tag_number                          ,
		gen_random_uuid()                              ,
		coalesce(xform.owner_full_name,' ')            ,
		coalesce(xform.owner_mailing_address, ' ')     ,
		coalesce(xform.owner_city, ' ')                ,
		coalesce(xform.owner_postal_code , ' ')        ,
		coalesce(xform.street_address    , ' ')        ,
		coalesce(xform.city              , ' ')        ,
		coalesce(xform.legal_lot         , ' ')        ,
		coalesce(xform.legal_plan        , ' ')        ,
		coalesce(xform.legal_district_lot, ' ')        ,
		coalesce(xform.legal_block       , ' ')        ,
		coalesce(xform.legal_section     , ' ')        ,
		coalesce(xform.legal_township    , ' ')        ,
		coalesce(xform.legal_range       , ' ')        ,
		xform.legal_pid                                ,
		coalesce(xform.well_location_description,' ')  ,
		xform.identification_plate_number              ,
		coalesce(xform.diameter, ' ')                  ,
		xform.total_depth_drilled                      ,
		xform.finished_well_depth                      ,
		xform.well_yield                               ,
		use.intended_water_use_guid                    ,
		land.land_district_guid                        ,
		xform.province_state_guid                      ,
		class.well_class_guid                          ,
		subclass.well_subclass_guid                    ,
		xform.well_yield_unit_guid                     ,
		xform.latitude                                 ,
		xform.longitude                                ,
		xform.ground_elevation                         ,
		xform.well_orientation                         ,
		' '                                            ,
		xform.drilling_method_guid                     ,
		xform.ground_elevation_method_guid             ,
		xform.when_created                             ,
		xform.when_updated                             ,
		xform.who_created                              ,
		xform.who_updated                              ,
		xform.bkfill_above_srfc_seal_depth             ,
		null                                           ,
		null                                           ,
		null                                           ,
		coalesce(xform.backfill_above_surface_seal,' '),
		well_status.well_status_guid                   ,
		licenced_status.well_licensed_status_guid      ,
		null                                           ,
		''                                             ,
		''                                             ,
		''                                             ,
		''                                             ,
		''                                             ,
		''                                             ,
		''                                             ,
		false                                          ,
		false                                          ,
		''                                             ,
		xform.construction_start_date                  ,
		xform.construction_end_date                    ,
		xform.alteration_start_date                    ,
		xform.alteration_end_date                      ,
		xform.decommission_start_date                  ,
		xform.decommission_end_date                    ,
		/*drilling_company.drilling_company_guid*/
    xform.final_casing_stick_up                    ,
    xform.artesian_flow
	FROM xform_gwells_well xform
	LEFT OUTER JOIN gwells_intended_water_use use ON xform.WELL_USE_CODE=use.code
	LEFT OUTER JOIN gwells_well_status well_status ON xform.STATUS_OF_WELL_CODE=upper(well_status.code)
	LEFT OUTER JOIN gwells_licensed_status licenced_status ON xform.WELL_LICENCE_GENERAL_STATUS=upper(licenced_status.code)
	LEFT OUTER JOIN gwells_land_district     land ON xform.LEGAL_LAND_DISTRICT_CODE=land.code
	INNER      JOIN gwells_well_class       class ON xform.CLASS_OF_WELL_CODCLASSIFIED_BY=class.code
	LEFT OUTER JOIN gwells_well_subclass subclass ON xform.SUBCLASS_OF_WELL_CLASSIFIED_BY=subclass.code AND subclass.well_class_guid = class.well_class_guid ;

  raise notice 'Preparing ETL report ...';

  SELECT count(*) from gwells_well into wells_rows;
  raise notice '... % rows loaded into the gwells_well table', 	wells_rows;
END;
$$ LANGUAGE plpgsql;
