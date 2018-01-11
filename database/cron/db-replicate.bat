@ECHO OFF
REM 2018-01-11 3:01:15 PM GW Windows batch file to emulate deploymeng on a local Windows 
REM                          environment.
REM
REM   This deploy is run only on the local Developer Windows environments 
REM
REM   Example: db-replicate.bat
REM
@ECHO ON
SET PGPASSWORD=%DATABASE_PASSWORD%


IF "%DB_REPLICATE%" == "" EXIT /B 1
IF "%DB_REPLICATE%" == "Subset" psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -c 'SELECT gwells_populate_xform(true);'
IF "%DB_REPLICATE%" == "Full" psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -c 'SELECT gwells_populate_xform(false);'

psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f - EOF
	\set AUTOCOMMIT off
	\echo '... clearing gwells_bcgs_number'
	TRUNCATE TABLE gwells_bcgs_number CASCADE;	
	SELECT gwells_migrate_bcgs();
	COMMIT;	
EOF

psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f - EOF
	\set AUTOCOMMIT off
	SELECT gwells_populate_well();	
	SELECT gwells_migrate_screens();
	SELECT gwells_migrate_production();
	SELECT gwells_migrate_casings();
	SELECT gwells_migrate_perforations();
	SELECT gwells_migrate_aquifers();
	SELECT gwells_migrate_lithology();
	DROP TABLE IF EXISTS xform_gwells_well;
	COMMIT;
EOF

EXIT /B 0