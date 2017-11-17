\echo '...importing wells_production_data data'
INSERT INTO gwells_production_data(
  production_data_guid           ,
  filing_number                  ,
  well_tag_number                ,
  yield_estimation_method_guid   ,
  yield_estimation_rate          ,
  yield_estimation_duration      ,
  yield_estimation_units         ,
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
  WELL.WELL_TAG_NUMBER                                                   ,
  YIELD_ESTIMATION_METHOD.yield_estimation_method_guid                   ,
  PRODUCTION_DATA.test_rate                                              ,
  PRODUCTION_DATA.test_duration                                          ,
  PRODUCTION_DATA.test_rate_units_code                                   ,
  PRODUCTION_DATA.static_level                                           ,
  PRODUCTION_DATA.net_drawdown                                           ,
  FALSE                                                                  ,
  PRODUCTION_DATA.who_created                                            ,
  PRODUCTION_DATA.when_created                                           ,
  coalesce(PRODUCTION_DATA.WHO_UPDATED,PRODUCTION_DATA.WHO_CREATED)      ,
  coalesce(PRODUCTION_DATA.WHEN_UPDATED,PRODUCTION_DATA.WHEN_CREATED)
FROM WELLS.WELLS_PRODUCTION_DATA PRODUCTION_DATA
     LEFT OUTER JOIN GWELLS_YIELD_ESTIMATION_METHOD YIELD_ESTIMATION_METHOD ON PRODUCTION_DATA.YIELD_ESTIMATED_METHOD_CODE=YIELD_ESTIMATION_METHOD.YIELD_ESTIMATION_METHOD_CODE
     INNER JOIN WELLS.WELLS_WELLS WELLS ON PRODUCTION_DATA.WELL_ID=WELLS.WELL_ID
     INNER JOIN GWELLS_WELL WELL ON WELLS.WELL_TAG_NUMBER = WELL.WELL_TAG_NUMBER
WHERE WELLS.ACCEPTANCE_STATUS_CODE NOT IN ('PENDING', 'REJECTED', 'NEW');

\echo 'wells_production_data data imported'

\t
SELECT count(*) || ' rows loaded into the gwells_production_data table' from gwells_production_data;
\t
