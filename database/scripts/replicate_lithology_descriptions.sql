DROP FUNCTION IF EXISTS migrate_lithology();

CREATE OR REPLACE FUNCTION migrate_lithology() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
  raise notice '...importing wells_lithology_descriptions data';

  INSERT INTO lithology_description(
    lithology_description_guid             ,
    filing_number                          ,
    well_tag_number                        ,
    lithology_from                         ,
    lithology_to                           ,
    lithology_raw_data                     ,
    lithology_description_code             ,
    lithology_material_code                ,
    lithology_hardness_code               ,
    lithology_colour_code                  ,
    water_bearing_estimated_flow           ,
    well_yield_unit_code                   ,
    lithology_observation                  ,
    lithology_sequence_number              ,
    create_user                            ,
    create_date                           ,
    update_user                            ,
    update_date
  )
  SELECT
    gen_random_uuid()                                       ,
    null                                                    ,
    xform.well_tag_number                                   ,
    wld.lithology_from                                      ,
    wld.lithology_to                                        ,
    wld.lithology_raw_data                                  ,
    wld.lithology_code                                      ,
    wld.lithology_material_code                             ,
    wld.relative_hardness_code                              ,
    wld.lithology_colour_code                               ,
    wld.water_bearing_estimated_flow                        ,
    CASE wld.water_bearing_est_flw_unt_cd
        WHEN 'USGM' THEN 'USGPM'
        ELSE wld.water_bearing_est_flw_unt_cd
    END AS well_yield_unit_code                             ,
    wld.lithology_observation                               ,
    wld.lithology_sequence_number                           ,
    wld.who_created                                         ,
    wld.when_created                                        ,
    COALESCE(wld.who_updated, wld.who_created)              ,
    COALESCE(wld.when_updated, wld.when_created)
  FROM wells.wells_lithology_descriptions wld
  INNER JOIN xform_well xform ON xform.well_id=wld.well_id
  INNER JOIN wells.wells_wells wells ON wells.well_id=wld.well_id;

  raise notice '...wells_lithology_descriptions data imported';
  SELECT count(*) from lithology_description into row_count;
  raise notice '% rows loaded into the lithology_description table',  row_count;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION migrate_lithology () IS 'Load Lithology, only for the wells that have been replicated.'; 