DROP FUNCTION IF EXISTS migrate_perforations();

CREATE OR REPLACE FUNCTION migrate_perforations() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
  raise notice '...importing wells_perforations data';
  INSERT INTO perforation(
    perforation_guid                   ,
    well_tag_number                    ,
    liner_thickness                    ,
    liner_diameter                     ,
    liner_from                         ,
    liner_to                           ,
    liner_perforation_from             ,
    liner_perforation_to               ,
    create_user, create_date, update_user, update_date
    )
  SELECT
    gen_random_uuid()                  ,
    xform.well_tag_number              ,
    perforations.liner_thickness       ,
    perforations.liner_diameter        ,
    perforations.liner_from            ,
    perforations.liner_to              ,
    perforations.liner_perforation_from,
    perforations.liner_perforation_to  ,
    perforations.who_created, perforations.when_created, perforations.who_updated, perforations.when_updated
  FROM wells.wells_perforations perforations
  INNER JOIN xform_well xform ON perforations.well_id=xform.well_id
  WHERE NOT (liner_from is  null
  AND liner_to               IS  NULL
  AND liner_diameter         IS  NULL
  AND liner_thickness        IS  NULL
  AND liner_perforation_from IS  NULL
  AND liner_perforation_to   IS  NULL);


  raise notice '...wells_perforations data imported';
  SELECT count(*) from perforation into row_count;
  raise notice '% rows loaded into the perforation table',  row_count;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION migrate_perforations () IS 'Load BCGS numbers, only for the wells that have been replicated.';
