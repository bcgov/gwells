DROP FUNCTION IF EXISTS migrate_production();

CREATE OR REPLACE FUNCTION migrate_production() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
  raise notice '...importing wells_production_data data';
  INSERT INTO production_data(
    production_data_guid           ,
    filing_number                  ,
    well_tag_number                ,
    yield_estimation_method_code   ,
    yield_estimation_rate          ,
    yield_estimation_duration      ,
    well_yield_unit_code           ,
    static_level                   ,
    drawdown                       ,
    hydro_fracturing_performed     ,
    create_user                    ,
    create_date                   ,
    update_user                    ,
    update_date
  )
  SELECT
    gen_random_uuid()                                                      ,
    null                                                                   ,
    xform.well_tag_number                                                  ,
    CASE production_data.yield_estimated_method_code
      WHEN 'UNK' THEN null
      ELSE production_data.yield_estimated_method_code
    END AS yield_estimation_method_code,
    production_data.test_rate                                              ,
    production_data.test_duration                                          ,
    CASE production_data.test_rate_units_code 
        WHEN 'USGM' THEN 'USGPM'
        ELSE production_data.test_rate_units_code 
    END AS well_yield_unit_code                                            ,
    production_data.static_level                                           ,
    production_data.net_drawdown                                           ,
    false                                                                  ,
    production_data.who_created                                            ,
    production_data.when_created                                           ,
    COALESCE(production_data.who_updated,production_data.who_created)      ,
    COALESCE(production_data.when_updated,production_data.when_created)
  FROM wells.wells_production_data production_data
  INNER JOIN xform_well xform ON production_data.well_id=xform.well_id;


  raise notice '...wells_production_data data imported';
  SELECT count(*) from production_data into row_count;
  raise notice '% rows loaded into the production_data table',  row_count;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION migrate_production () IS 'Load Production Data, only for the wells that have been replicated.'; 