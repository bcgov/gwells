DROP FUNCTION IF EXISTS gwells_migrate_aquifers();

CREATE OR REPLACE FUNCTION gwells_migrate_aquifers() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
  raise notice '...importing gw_aquifer_wells data';

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
    xform.well_tag_number                         ,
    aws.who_created                               ,
    aws.when_created                              ,
    coalesce(aws.who_updated, aws.who_created)    ,
    coalesce(aws.when_updated, aws.when_created)
  -- GW Sat Dec  9 19:31:02 2017 changed LEFT OUTER JOIN to INNER JOIN
  --        As those aquifers are for WELLS that are one of ('PENDING', 'REJECTED', 'NEW')  
  FROM wells.gw_aquifer_wells aws INNER JOIN xform_gwells_well xform ON aws.well_id = xform.well_id;

  raise notice 'gw_aquifer_well data imported';
  SELECT count(*) from gwells_aquifer_well into row_count;
  raise notice '... % rows loaded into the gwells_aquifer_well table',  row_count;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION gwells_migrate_aquifers () IS 'Load Aquifer Wells, only for the wells that have been replicated.'; 