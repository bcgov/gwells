DROP FUNCTION IF EXISTS migrate_aquifers();

CREATE OR REPLACE FUNCTION migrate_aquifers() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
  raise notice '...importing gw_aquifer_wells data';

  INSERT INTO aquifer_well(
    aquifer_well_guid                             , --> PK
    aquifer_id                                    ,
    well_tag_number                               ,  -->FK for now -- moving to well_guid later
    create_user                                   ,
    create_date                                  ,
    update_user                                   ,
    update_date)
  SELECT
    gen_random_uuid()                             ,
    aws.aquifer_id                                ,
    xform.well_tag_number                         ,
    aws.who_created                               ,
    aws.when_created                              ,
    coalesce(aws.who_updated, aws.who_created)    ,
    coalesce(aws.when_updated,aws.when_created)
  FROM wells.gw_aquifer_wells aws INNER JOIN xform_well xform ON aws.well_id = xform.well_id;

  raise notice '...gw_aquifer_well data imported';
  SELECT count(*) from aquifer_well into row_count;
  raise notice '% rows loaded into the aquifer_well table',  row_count;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION migrate_aquifers () IS 'Load Aquifer Wells, only for the wells that have been replicated.'; 