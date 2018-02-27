DROP FUNCTION IF EXISTS gwells_migrate_screens();

CREATE OR REPLACE FUNCTION gwells_migrate_screens() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
  raise notice '...importing wells_screens data';

  INSERT INTO gwells_screen(
    screen_guid                                   , -->PK
    filing_number                                 , -->FK
    well_tag_number                               , -->FK
    screen_from                                   ,
    screen_to                                     ,
    internal_diameter                             ,
    screen_assembly_type_guid                     , -->FK
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
    screen_assembly_type.screen_assembly_type_guid,
    screens.screen_slot_size                      ,
    screens.when_created                          ,
    screens.when_updated                          ,
    screens.who_created                           ,
    screens.who_updated
  FROM wells.wells_screens screens
       INNER JOIN xform_gwells_well xform ON xform.well_id=screens.well_id
       LEFT OUTER JOIN screen_assembly_type_code screen_assembly_type ON
       ( screens.screen_assembly_type_code=screen_assembly_type.screen_assembly_type_code OR
         screens.screen_assembly_type_code='L' AND screen_assembly_type.screen_assembly_type_code='LEAD' OR
         screens.screen_assembly_type_code='K  & Riser' AND screen_assembly_type.screen_assembly_type_code='K_RISER'
       );

  raise notice '...wells_screens data imported';
  SELECT count(*) from gwells_screen into row_count;
  raise notice '% rows loaded into the gwells_screen table',  row_count;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION gwells_migrate_screens () IS 'Load Screen details numbers, only for the wells that have been replicated.'; 