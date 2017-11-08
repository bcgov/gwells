INSERT INTO gwells_bcgs_Numbers(
  bcgs_id,
  bcgs_number,
  who_created,
  when_created,
  who_updated,
  when_updated
)
SELECT
bcgs_id,
bcgs_number,
who_created,
when_created,
who_updated,
when_updated
FROM wells.wells_bcgs_numbers;
