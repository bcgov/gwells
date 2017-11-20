\echo '...importing gw_aquifer_wells data'

INSERT INTO gwells_aquifer_well(
  aquifer_well_guid                             , --> PK
  aquifer_id                                    ,
  well_tag_number                               ,  -->FK for now -- moving to well_guid later
  who_created                                   ,
  when_created                                  ,
  who_updated                                   ,
  when_updated)
SELECT
  gen_random_uuid()                             ,
  aws.aquifer_id                                ,
  wells.well_tag_number                         ,
  aws.who_created                               ,
  aws.when_created                              ,
  coalesce(aws.who_updated, aws.who_created)    ,
  coalesce(aws.when_updated, aws.when_created)
FROM
  wells.gw_aquifer_wells aws LEFT OUTER JOIN wells.wells_wells wells ON aws.well_id = wells.well_id
                            INNER JOIN gwells_well well ON well.well_tag_number = wells.well_tag_number
WHERE wells.acceptance_status_code NOT IN ('PENDING', 'REJECTED', 'NEW');

\echo 'gw_aquifer_well data imported'

\t
SELECT count(*) || ' rows loaded into the gwells_aquifer_well table' from gwells_aquifer_well;
\t
