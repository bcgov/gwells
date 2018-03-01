DROP FUNCTION IF EXISTS migrate_screens();

CREATE OR REPLACE FUNCTION migrate_screens() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
  raise notice '...importing wells_screens data';

  INSERT INTO screen(
    screen_guid                                   , -->PK
    filing_number                                 , -->FK
    well_tag_number                               , -->FK
    screen_from                                   ,
    screen_to                                     ,
    internal_diameter                             ,
    screen_assembly_type_code                     , 
    slot_size                                     ,
    create_date                                  ,
    update_date                                  ,
    create_user                                   ,
    update_user)
  SELECT
    gen_random_uuid()                             ,
    null                                          ,
    xform.well_tag_number                         ,
    screens.screen_from                           ,
    screens.screen_to                             ,
    screens.screen_internal_diameter              ,
    CASE screens.screen_assembly_type_code
      WHEN 'L'          THEN 'LEAD'
      WHEN 'K  & Riser' THEN 'K_RISER'
      ELSE screens.screen_assembly_type_code
    END AS screen_assembly_type_code ,
    screens.screen_slot_size                      ,
    screens.when_created                          ,
    screens.when_updated                          ,
    screens.who_created                           ,
    screens.who_updated
  FROM wells.wells_screens screens
  INNER JOIN xform_well xform ON xform.well_id=screens.well_id;

  raise notice '...wells_screens data imported';
  SELECT count(*) from screen into row_count;
  raise notice '% rows loaded into the screen table',  row_count;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION migrate_screens () IS 'Load Screen details numbers, only for the wells that have been replicated.'; 