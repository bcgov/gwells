\echo '...importing wells_lithology_descriptions data'
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
  who_created                            ,
  when_created                           ,
  who_updated                            ,
  when_updated
)
SELECT
  gen_random_uuid()                                         ,
  null                                                      ,
  wells.well_tag_number                                         ,
  wld.lithology_from                                        ,
  wld.lithology_to                                          ,
  wld.lithology_raw_data                                    ,
  lithology_description_code.lithology_description_code_guid,
  lithology_material.lithology_material_guid                ,
  lithology_hardness.lithology_hardness_guid                ,
  lithology_colour.lithology_colour_guid                    ,
  wld.water_bearing_estimated_flow                          ,
  well_yield_unit.well_yield_unit_guid                      ,
  wld.lithology_observation                                 ,
  wld.lithology_sequence_number                             ,
  wld.who_created                                           ,
  wld.when_created                                          ,
  COALESCE(wld.who_updated, wld.who_created)                ,
  COALESCE(wld.when_updated, wld.when_created)
FROM wells.wells_lithology_descriptions wld INNER JOIN wells.wells_wells wells ON wells.well_id=wld.well_id
                                           INNER JOIN gwells_well well ON well.well_tag_number = wells.well_tag_number
                                           LEFT OUTER JOIN gwells_lithology_hardness lithology_hardness ON UPPER(wld.relative_hardness_code)=UPPER(lithology_hardness.code)
                                           LEFT OUTER JOIN gwells_lithology_colour lithology_colour ON UPPER(wld.lithology_colour_code)=UPPER(lithology_colour.code)
                                           LEFT OUTER JOIN gwells_well_yield_unit well_yield_unit ON UPPER(wld.water_bearing_est_flw_unt_cd)=UPPER(well_yield_unit.code)
                                           LEFT OUTER JOIN gwells_lithology_material lithology_material ON UPPER(wld.lithology_material_code)=UPPER(lithology_material.code)
                                           LEFT OUTER JOIN gwells_lithology_description_code lithology_description_code ON UPPER(wld.lithology_code)=UPPER(lithology_description_code.code)
WHERE wells.acceptance_status_code NOT IN ('PENDING', 'REJECTED', 'NEW') AND
      (lithology_description_id != 257638 AND wells.well_id != 54374)  AND
      (lithology_description_id != 252021 AND wells.well_id != 55879)  AND
      (lithology_description_id != 239976 AND wells.well_id != 8622)   AND
      (lithology_description_id != 67414  AND wells.well_id != 59726 )  AND
      (lithology_description_id != 67415  AND wells.well_id != 59726 )  AND
      (lithology_description_id != 67090  AND wells.well_id != 21728 )  AND
      (lithology_description_id != 67119  AND wells.well_id != 21732 )  AND
      (lithology_description_id != 628025 AND wells.well_id != 113892) AND
      (lithology_description_id != 628026 AND wells.well_id != 113892) AND
      (lithology_description_id != 628027 AND wells.well_id != 113893) AND
      (lithology_description_id != 628028 AND wells.well_id != 113894) AND
      (lithology_description_id != 628029 AND wells.well_id != 113895) AND
      (lithology_description_id != 631336 AND wells.well_id != 114455);

\echo 'wells_lithology_descriptions data imported'

\t
SELECT count(*) || ' rows loaded into the gwells_lithology_description table' from gwells_lithology_description;
\t
