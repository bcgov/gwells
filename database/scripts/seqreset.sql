BEGIN;
SELECT setval(pg_get_serial_sequence('"gwells_activity_submission"','filing_number'), coalesce(max("filing_number"), 1), max("filing_number") IS NOT null) FROM "gwells_activity_submission";
SELECT setval(pg_get_serial_sequence('"gwells_well"','well_tag_number'), coalesce(max("well_tag_number"), 1), max("well_tag_number") IS NOT null) FROM "gwells_well";
COMMIT;
