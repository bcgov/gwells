\echo '...importing gw_aquifer_wells data'

INSERT INTO AquiferWell(
  aquifer_well_guid                             , --> PK
  aquifer_id                                    ,
  well_tag_number)                                -->FK for now -- moving to well_guid later
SELECT
  gen_random_uuid()                             ,
  gaw.aquifer_id                                ,
  wells.well_tag_number                         
FROM
  wells.gw_aquifer_wells gaw LEFT OUTER JOIN wells.wells_wells wells ON gaw.well_id = wells.well_id
