DROP FUNCTION IF EXISTS gwells_migrate_production();

CREATE OR REPLACE FUNCTION gwells_migrate_production() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
  raise notice '...importing wells_production_data data';
  INSERT INTO gwells_production_data(
    production_data_guid           ,
    filing_number                  ,
    well_tag_number                ,
    yield_estimation_method_guid   ,
    yield_estimation_rate          ,
    yield_estimation_duration      ,
    well_yield_unit_guid           ,
    static_level                   ,
    drawdown                       ,
    hydro_fracturing_performed     ,
    who_created                    ,
    when_created                   ,
    who_updated                    ,
    when_updated
  )
  SELECT
    gen_random_uuid()                                                      ,
    null                                                                   ,
    xform.well_tag_number                                                  ,
    yield_estimation_method.yield_estimation_method_guid                   ,
    production_data.test_rate                                              ,
    production_data.test_duration                                          ,
    CASE production_data.test_rate_units_code
      WHEN 'GPM'  THEN 'c4634ef447c311e7a91992ebcb67fe33'::uuid
      WHEN 'IGM'  THEN 'c4634ff847c311e7a91992ebcb67fe33'::uuid
      WHEN 'DRY'  THEN 'c46347b047c311e7a91992ebcb67fe33'::uuid
      WHEN 'LPS'  THEN 'c46350c047c311e7a91992ebcb67fe33'::uuid
      WHEN 'USGM' THEN 'c463525047c311e7a91992ebcb67fe33'::uuid
      WHEN 'GPH'  THEN 'c4634b4847c311e7a91992ebcb67fe33'::uuid
      WHEN 'UNK'  THEN 'c463518847c311e7a91992ebcb67fe33'::uuid
      ELSE 'c463518847c311e7a91992ebcb67fe33'::uuid -- As PostGres didn't like "" as guid value
    END AS well_yield_unit_guid                                            ,
    production_data.static_level                                           ,
    production_data.net_drawdown                                           ,
    false                                                                  ,
    production_data.who_created                                            ,
    production_data.when_created                                           ,
    COALESCE(production_data.who_updated,production_data.who_created)      ,
    COALESCE(production_data.when_updated,production_data.when_created)
  FROM wells.wells_production_data production_data
       INNER JOIN xform_gwells_well xform ON production_data.well_id=xform.well_id
       LEFT OUTER JOIN gwells_yield_estimation_method yield_estimation_method ON production_data.yield_estimated_method_code=yield_estimation_method.yield_estimation_method_code;


  raise notice 'wells_production_data data imported';
  SELECT count(*) from gwells_production_data into row_count;
  raise notice '... % rows loaded into the gwells_production_data table',  row_count;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION gwells_migrate_production () IS 'Load Production Data, only for the wells that have been replicated.'; 