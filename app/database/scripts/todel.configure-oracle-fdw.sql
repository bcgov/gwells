BEGIN;
CREATE EXTENSION IF NOT EXISTS oracle_fdw;

DROP SERVER IF EXISTS wells_oradb CASCADE;
CREATE SERVER wells_oradb FOREIGN DATA WRAPPER oracle_fdw OPTIONS (dbserver '//nrk1-scan.bcgov/envprod1.nrs.bcgov');


DROP USER MAPPING IF EXISTS FOR public SERVER wells_oradb;
CREATE USER MAPPING FOR public SERVER wells_oradb OPTIONS (user '<proxy-user>', password '<proxy-password>');

DROP SCHEMA IF EXISTS wells;
CREATE SCHEMA wells;

IMPORT FOREIGN SCHEMA "WELLS" FROM SERVER wells_oradb INTO wells;

DROP ROLE IF EXISTS wells_legacy_read;
CREATE ROLE wells_legacy_read;
GRANT USAGE ON SCHEMA wells TO wells_legacy_read;

GRANT SELECT ON ALL TABLES IN SCHEMA wells TO wells_legacy_read;
GRANT wells_legacy_read to gwells;

COMMIT;
