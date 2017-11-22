BEGIN;
SELECT setval(pg_get_serial_sequence('"well_water_quality"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "well_water_quality";
SELECT setval(pg_get_serial_sequence('"well"','well_tag_number'), coalesce(max("well_tag_number"), 1), max("well_tag_number") IS NOT null) FROM "well";
SELECT setval(pg_get_serial_sequence('"activity_submission_water_quality"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "activity_submission_water_quality";
SELECT setval(pg_get_serial_sequence('"activity_submission"','filing_number'), coalesce(max("filing_number"), 1), max("filing_number") IS NOT null) FROM "activity_submission";
COMMIT;
