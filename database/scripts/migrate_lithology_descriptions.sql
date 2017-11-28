\echo '...importing wells_lithology_description data'
INSERT INTO gwells_lithology_description(
  lithology_description_guid        ,
  activity_submission_guid          ,
  well_tag_number                   ,
  lithology_from                    ,
  lithology_to                      ,
  lithology_raw_data                ,
  lithology_description_guid        ,
  lithology_hardness_guid           ,
  lithology_colour_guid             ,
  water_bearing_estimated_flow      ,
  water_bearing_estimated_flow_units,
  lithology_observation
)
SELECT
  gen_random_uuid(),
  null,
  w.well_tag_number,
  lithology_from,
  lithology_to,
  lithology_raw_data,
  lithology_description_guid,
  lithology_hardness_guid,
  lithology_colour_guid,
  water_bearing_estimated_flow,
  water_bearing_est_flw_unt_cd,
  lithology_observations
FROM wells.wells_lithology_description wld INNER JOIN wells.wells_wells w ON w.well_id=wld.well_id
                                           LEFT OUTER JOIN wells.wells_lithology_description_codes wldc ON wld.lithology_description_code=wldc.lithology_description_code
                                           LEFT OUTER JOIN gwells_lithology_description gld ON wldc.lithology_description_code = gld.lithology_description_code
                                           LEFT OUTER JOIN wells.wells_lithology_hardness_codes wlhc ON wldc.lithology_hardess_code = wlhc.lithology_hardness_code
                                           LEFT OUTER JOIN gwells_lithology_hardness glh ON wldc.lithology_hardness_code = glh.lithology_hardness_code
                                           LEFT OUTER JOIN wells.wells_lithology_colour_codes wlcc ON wld.lithology_colour_code=wlcc.lithology_colour_code
                                           LEFT OUTER JOIN gwells_lithology_colour glc ON wld.lithology_colour_code=gls.lithology_colour_code;

\echo 'wells_lithology_description data imported'

\t
SELECT count(*) || ' rows loaded into the gwells_lithology_description table' from gwells_lithology_description;
\t
