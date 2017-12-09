\echo '...importing wells_production_data data'
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
  wells.well_tag_number                                                   ,
  yield_estimation_method.yield_estimation_method_guid                   ,
  production_data.test_rate                                              ,
  production_data.test_duration                                          ,
  well_yield_unit.well_yield_unit_guid                                   ,
  production_data.static_level                                           ,
  production_data.net_drawdown                                           ,
  false                                                                  ,
  production_data.who_created                                            ,
  production_data.when_created                                           ,
  COALESCE(production_data.who_updated,production_data.who_created)      ,
  COALESCE(production_data.when_updated,production_data.when_created)
FROM wells.wells_production_data production_data
     LEFT OUTER JOIN gwells_yield_estimation_method yield_estimation_method ON production_data.yield_estimated_method_code=yield_estimation_method.yield_estimation_method_code
     LEFT OUTER JOIN gwells_well_yield_unit well_yield_unit ON production_data.test_rate_units_code=well_yield_unit.code
     INNER JOIN wells.wells_wells wells ON production_data.well_id=wells.well_id
WHERE wells.acceptance_status_code NOT IN ('PENDING', 'REJECTED', 'NEW')
:xform_filter
;

\echo 'wells_production_data data imported'

\t
SELECT count(*) || ' rows loaded into the gwells_production_data table' from gwells_production_data;
\t
