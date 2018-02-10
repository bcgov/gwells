DROP FUNCTION IF EXISTS gwells_migrate_perforations();

CREATE OR REPLACE FUNCTION gwells_migrate_perforations() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
  raise notice '...importing wells_perforations data';
  INSERT INTO gwells_perforation(
    perforation_guid                   ,
    well_tag_number                    ,
    liner_thickness                    ,
    liner_diameter                     ,
    liner_from                         ,
    liner_to                           ,
    liner_perforation_from             ,
    liner_perforation_to               ,
    create_user                        ,
    create_date                       ,
    update_user                        ,
    update_date
  ) SELECT
    gen_random_uuid()                  ,
    xform.well_tag_number              ,
    perforations.liner_thickness       ,
    perforations.liner_diameter        ,
    perforations.liner_from            ,
    perforations.liner_to              ,
    perforations.liner_perforation_from,
    perforations.liner_perforation_to  ,
    perforations.who_created           ,
    perforations.when_created          ,
    perforations.who_updated           ,
    perforations.when_updated
  FROM wells.wells_perforations perforations
  INNER JOIN xform_gwells_well xform ON perforations.well_id=xform.well_id;


  raise notice '...wells_perforations data imported';
  SELECT count(*) from gwells_perforation into row_count;
  raise notice '% rows loaded into the gwells_perforation table',  row_count;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION gwells_migrate_perforations () IS 'Load BCGS numbers, only for the wells that have been replicated.'; 