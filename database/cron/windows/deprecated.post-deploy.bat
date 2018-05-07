@ECHO OFF
REM  Mon Nov  6 15:03:49 2017 GW script run by locally on your Windows machine
REM 
REM    If run on local Developer workstation, ensure that you have Environment variables set
REM    for $DATABASE_PASSWORD, %DATABASE_NAME%, %DATABASE_USER%, it is assumed that you use
REM	   the Postgresql server on your localhost
REM 
echo "Running Post-Deploy tasks..."
set PGPASSWORD=%DATABASE_PASSWORD%
cd ..\..\scripts\
echo ". Creating additional DB objects (e.g. spatial indices, stored functions)"
psql -d %DATABASE_NAME% -U %DATABASE_USER% -f post-deploy.sql
psql -d %DATABASE_NAME% -U %DATABASE_USER% -f populate-xform-gwells-well.sql
psql -d %DATABASE_NAME% -U %DATABASE_USER% -f replicate_bcgs.sql
psql -d %DATABASE_NAME% -U %DATABASE_USER% -f populate-gwells-well-from-xform.sql
psql -d %DATABASE_NAME% -U %DATABASE_USER% -f replicate_screens.sql
psql -d %DATABASE_NAME% -U %DATABASE_USER% -f replicate_production_data.sql
psql -d %DATABASE_NAME% -U %DATABASE_USER% -f replicate_casings.sql
psql -d %DATABASE_NAME% -U %DATABASE_USER% -f replicate_perforations.sql
psql -d %DATABASE_NAME% -U %DATABASE_USER% -f replicate_aquifer_wells.sql
psql -d %DATABASE_NAME% -U %DATABASE_USER% -f replicate_lithology_descriptions.sql
psql -d %DATABASE_NAME% -U %DATABASE_USER% -f db_replicate.sql

cd ..\codetables\wellsearch
REM Refresh Code lookup tables, including the well table
psql -d %DATABASE_NAME% -U %DATABASE_USER% -f clear-tables.sql
psql -d %DATABASE_NAME% -U %DATABASE_USER% -f data-load-static-codes.sql

echo ". Running DB Replication from Legacy Database, as per DB_REPLICATION flag"
cd ..\cron\
psql -d %DATABASE_NAME% -U %DATABASE_USER% -f db_replicate.sql

echo "Completed Post-Deploy tasks."
@ECHO ON