# Database Scripts

## Load from legacy Oracle database

The legacy database is WELLS schema of ENVPROD1.NRS.GOV.BC.CA, and was exported using SQL Developer (via [Citrix](https://dts.gov.bc.ca/Citrix/BCGOVWeb/) *Kamloops Desktop - ArcGIS 10-2* desktop).

## Loading legacy data 

The legacy data was exported into human-readable CSV files, and stored outsitde of this github repo.

1. Sync scripts to Postgres pod (from developer workstation):
    `oc rsync /Users/garywong/projects/gwells/github/database postgresql-2-2vvoh:/tmp`

2.  Sync legacy CSV files to Postgres pod (from developer workstation):
    `oc rsync /Users/garywong/projects/gwells/legacy-data postgresql-2-2vvoh:/tmp`

3.  Remote into Postgres pod (from developer workstation).  Note that the the pod name changew with
each pod deployment, so get the name first (i.e. *oc get pods*):
    `oc rsh postgresql-2-2vvoh`

4.  From the remote shell into the Postgres pod:
    ```
    cd /tmp  
    psql -d gwells -U userGN0  -f ./database/scripts/drop-tables-cascade.sql 
    psql -d gwells -U userGN0  -f ./database/scripts/create-tables.sql
    psql -d gwells -U userGN0  -f ./database/scripts/load-legacy-data.1-of-2.sql 
    psql -d gwells -U userGN0  -f ./database/scripts/load-legacy-data.2-of-2.sql 
    psql -d gwells -U userGN0  -f ./database/scripts/create-constraints.sql 
    ```

5. Run the psql client to verify the database objects:
    `psql -d gwells -U userGN0`
