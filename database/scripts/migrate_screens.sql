INSERT INTO gwells_screen(
screen_guid                                   , -->PK
filing_number                                 , -->FK
well_tag_number                               , -->FK
screen_from                                   ,
screen_to                                     ,
internal_diameter                             ,
screen_assembly_type_guid                     , -->FK
slot_size                                     ,
when_created                                  ,
when_updated                                  ,
who_created                                   ,
who_updated)
SELECT
gen_random_uuid()                             ,
null                                          ,
screens.well_id                               ,
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
     LEFT OUTER JOIN gwells_screen_assembly_type screen_assembly_type ON screens.screen_assembly_type_code=screen_assembly_type.screen_assembly_type_code
     INNER JOIN wells.wells_wells wells ON wells.well_tag_number=screens.well_id
WHERE WELLS.ACCEPTANCE_STATUS_CODE != 'REJECTED';
