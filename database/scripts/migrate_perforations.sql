\echo '...importing wells_perforations data'
INSERT INTO gwells_perforation(
  perforation_guid                   ,
  well_tag_number                    ,
  liner_thickness                    ,
  liner_diameter                     ,
  liner_from                         ,
  liner_to                           ,
  liner_perforation_from             ,
  liner_perforation_to               ,
  who_created                        ,
  when_created                       ,
  who_updated                        ,
  when_updated
) SELECT
  gen_random_uuid()                  ,
  wells.well_tag_number              ,
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
     INNER JOIN gwells_well well ON well.well_tag_number = perforations.well_id
     INNER JOIN wells.wells_wells wells on perforations.well_id=wells.well_id;

\echo 'wells_perforations data imported'

\t
SELECT count(*) || ' rows loaded into the gwells_perforation table' from gwells_perforation;
\t
