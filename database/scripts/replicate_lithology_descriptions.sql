DROP FUNCTION IF EXISTS gwells_migrate_lithology();

CREATE OR REPLACE FUNCTION gwells_migrate_lithology() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
  raise notice '...importing wells_lithology_descriptions data';

  INSERT INTO gwells_lithology_description(
    lithology_description_guid             ,
    filing_number                          ,
    well_tag_number                        ,
    lithology_from                         ,
    lithology_to                           ,
    lithology_raw_data                     ,
    lithology_description_code_guid        ,
    lithology_material_guid                ,
    lithology_hardness_guid                ,
    lithology_colour_guid                  ,
    water_bearing_estimated_flow           ,
    well_yield_unit_guid                   ,
    lithology_observation                  ,
    lithology_sequence_number              ,
    create_user                            ,
    create_date                           ,
    update_user                            ,
    update_date
  )
  SELECT
    gen_random_uuid()                                         ,
    null                                                      ,
    xform.well_tag_number                                     ,
    wld.lithology_from                                        ,
    wld.lithology_to                                          ,
    wld.lithology_raw_data                                    ,
    lithology_description_code.lithology_description_code_guid,
    lithology_material.lithology_material_guid                ,
    lithology_hardness.lithology_hardness_guid                ,
    lithology_colour.lithology_colour_guid                    ,
    wld.water_bearing_estimated_flow                          ,
    CASE wells.yield_unit_code
      WHEN 'GPM'  THEN 'c4634ef447c311e7a91992ebcb67fe33'::uuid
      WHEN 'IGM'  THEN 'c4634ff847c311e7a91992ebcb67fe33'::uuid
      WHEN 'DRY'  THEN 'c46347b047c311e7a91992ebcb67fe33'::uuid
      WHEN 'LPS'  THEN 'c46350c047c311e7a91992ebcb67fe33'::uuid
      WHEN 'USGM' THEN 'c463525047c311e7a91992ebcb67fe33'::uuid
      WHEN 'GPH'  THEN 'c4634b4847c311e7a91992ebcb67fe33'::uuid
      WHEN 'UNK'  THEN 'c463518847c311e7a91992ebcb67fe33'::uuid
      ELSE 'c463518847c311e7a91992ebcb67fe33'::uuid -- As PostGres didn't like "" as guid value
    END AS well_yield_unit_guid                               ,
    wld.lithology_observation                                 ,
    wld.lithology_sequence_number                             ,
    wld.who_created                                           ,
    wld.when_created                                          ,
    COALESCE(wld.who_updated, wld.who_created)                ,
    COALESCE(wld.when_updated, wld.when_created)
  FROM wells.wells_lithology_descriptions wld
  INNER JOIN xform_gwells_well xform ON xform.well_id=wld.well_id
  INNER JOIN wells.wells_wells wells ON wells.well_id=wld.well_id
  LEFT OUTER JOIN lithology_hardness_code lithology_hardness ON UPPER(wld.relative_hardness_code)=UPPER(lithology_hardness.code)
  LEFT OUTER JOIN lithology_colour_code lithology_colour ON UPPER(wld.lithology_colour_code)=UPPER(lithology_colour.code)
  LEFT OUTER JOIN gwells_well_yield_unit well_yield_unit ON UPPER(wld.water_bearing_est_flw_unt_cd)=UPPER(well_yield_unit.code)
  LEFT OUTER JOIN gwells_lithology_material lithology_material ON UPPER(wld.lithology_material_code)=UPPER(lithology_material.code)
  LEFT OUTER JOIN gwells_lithology_description_code lithology_description_code ON UPPER(wld.lithology_code)=UPPER(lithology_description_code.code);

  raise notice '...wells_lithology_descriptions data imported';
  SELECT count(*) from gwells_lithology_description into row_count;
  raise notice '% rows loaded into the gwells_lithology_description table',  row_count;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION gwells_migrate_lithology () IS 'Load Lithology, only for the wells that have been replicated.'; 