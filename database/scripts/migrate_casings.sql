\echo '...importing wells_casings data'
INSERT INTO gwells_casing(
casing_guid                                   , -->PK
filing_number                                 , -->FK
well_tag_number                               , -->FK
casing_from                                   ,
casing_to                                     ,
internal_diameter                             ,
casing_material_guid                          , -->FK
wall_thickness                                ,
drive_shoe                                    ,
when_created                                  ,
when_updated                                  ,
who_created                                   ,
who_updated)
SELECT
    gen_random_uuid()                             ,
    null                                          ,
    wells.well_tag_number                         ,
    casings.casing_from                           ,
    casings.casing_to                             ,
    casings.casing_size                           ,
    casing_material.casing_material_guid          ,
    casings.casing_wall                           ,
    CASE casings.casing_drive_shoe_ind
        WHEN '' THEN null
        WHEN 'Y' THEN TRUE
        WHEN 'N' THEN FALSE
    END                                           ,
    casings.when_created                          ,
    casings.when_updated                          ,
    casings.who_created                           ,
    casings.who_updated
FROM wells.wells_casings casings
     LEFT OUTER JOIN gwells_casing_material casing_material ON casings.casing_material_code=casing_material.casing_material_code
     INNER JOIN wells.wells_wells wells ON wells.well_id=casings.well_id
     INNER JOIN gwells_well well ON well.well_tag_number = wells.well_tag_number
WHERE wells.acceptance_status_code NOT IN ('PENDING', 'REJECTED', 'NEW');

\echo 'wells_casings data imported'

\t
SELECT count(*) || ' rows loaded into the gwells_casing table' from gwells_casing;
\t
