DROP FUNCTION IF EXISTS migrate_casings();

CREATE OR REPLACE FUNCTION migrate_casings() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
    raise notice '...importing wells_casings data';

    INSERT INTO casing(
    casing_guid         , -->PK
    filing_number       , -->FK
    well_tag_number     , -->FK
    casing_from         ,
    casing_to           ,
    diameter            ,
    casing_material_code,   
    wall_thickness      ,
    drive_shoe          ,
    create_date         ,
    update_date         ,
    create_user         ,
    update_user)
    SELECT
        gen_random_uuid()                 ,
        null                              ,
        xform.well_tag_number             ,
        casings.casing_from               ,
        casings.casing_to                 ,
        casings.casing_size               ,
        casings.casing_material_code      ,
        casings.casing_wall               ,
        CASE casings.casing_drive_shoe_ind
            WHEN '' THEN null
            WHEN 'Y' THEN TRUE
            WHEN 'N' THEN FALSE
        END                               ,
        casings.when_created              ,
        casings.when_updated              ,
        casings.who_created               ,
        casings.who_updated
    FROM wells.wells_casings casings 
    INNER JOIN xform_well xform ON xform.well_id=casings.well_id;

  raise notice '...wells_casings data imported';
  SELECT count(*) from casing into row_count;
  raise notice '% rows loaded into the casing table',  row_count;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION migrate_casings () IS 'Load Casing details, only for the wells that have been replicated.'; 