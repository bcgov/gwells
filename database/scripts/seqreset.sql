BEGIN;
SELECT setval(pg_get_serial_sequence('"gwells_province_state"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "gwells_province_state";
SELECT setval(pg_get_serial_sequence('"gwells_land_district"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "gwells_land_district";
SELECT setval(pg_get_serial_sequence('"gwells_well_yield_unit"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "gwells_well_yield_unit";
SELECT setval(pg_get_serial_sequence('"gwells_well_owner"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "gwells_well_owner";
SELECT setval(pg_get_serial_sequence('"gwells_well"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "gwells_well";
COMMIT;
