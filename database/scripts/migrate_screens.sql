INSERT INTO gwells_screen(
screen_guid                                   , -->PK
activity_submission_guid                      , -->FK
well                                          , -->FK
screen_from                                   ,
screen_to                                     ,
internal_diameter                             ,
assembly_type_guid                            , -->FK
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
screens.slot_size                             
FROM wells.screens screens
     LEFT OUTER JOIN gwells_screen_assembly_type screen_assembly_type ON screens.screen_assembly_code=screen_assembly_type.screen_assembly_code
