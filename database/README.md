# Database Scripts

## Export from the legacy Oracle database

The legacy database is WELLS schema of ENVPROD1.NRS.GOV.BC.CA, and was exported using SQL Developer (via [Citrix](https://dts.gov.bc.ca/Citrix/BCGOVWeb/) *Kamloops Desktop - ArcGIS 10-2* desktop).

1. Copy the transformation (e.g. transforms the data while exporting to CSV) script to your H:\ drive (i.e. it will automatically be visible from Citrix):
    [xform-legacy-data.sql](scripts/sql-developer/xform-legacy-data.sql)

2. From the Windows Start Menu, open Oracle SQL*Developer
    Start -> All Programs -> Oracle Tools -> Oracle SQL Developer

3. Login to ENVPROD1.NRS.GOV.BC.CA with an Oracle DB Account that can view WELLS schema objects

4.  Navigate to the Oracle SQL Develoepr WorkSheet tab and enter the path of the copied transformation script:
    `@h:\tmp\xform-legacy-data.sql`

    Three CSV files will be created:
    ```
    land_district.csv
    well_owner.csv
    well.csv
    ```

5. Copy the CSV files over to your local workstation, ready to be included in the `rsync` [step below](#rsync-csv).

## Loading data upon which to run a live Search 

The legacy data was exported into human-readable CSV files, and stored outsitde of this github repo.
The seqreset.sql script was generated via Django using:
    `python manage.py sqlsequencereset gwells > ./database/scripts/seqreset.sql`

1. Sync scripts to Postgres pod (from developer workstation):

    `oc rsync /Users/garywong/projects/gwells/github/database postgresql-2-2vvoh:/tmp`


2.  Sync all CSV files to Postgres pod (from developer workstation) <a id="rsync-csv"></a>:

    `oc rsync /Users/garywong/projects/gwells/legacy-data/postgres postgresql-2-2vvoh:/tmp`

3.  Remote into Postgres pod (from developer workstation).  Note that the the pod name changew with
each pod deployment, so get the name first (i.e. *oc get pods*) from the correct project (dev/test/prod):

    `oc rsh postgresql-2-2vvoh`

4.  From the remote shell into the Postgres pod:
    ```
    cd /tmp/  
    psql -d gwells -U <user>  -f ./database/scripts/drop-tables-cascade.sql 
    psql -d gwells -U <user>  -f ./database/scripts/create-tables.sql
    psql -d gwells -U <user>  -f ./database/scripts/load-search-ready-data.sql
    psql -d gwells -U <user>  -f ./database/scripts/create-constraints.sql
    psql -d gwells -U <user>  -f ./database/scripts/seqreset.sql 
    ```

5. Run the psql client to verify the database objects:
    `psql -d gwells -U userGN0`

## Clear all data from which the live Search ran

Repeat steps 1-3, and then:

4.  From the remote shell into the Postgres pod:
    ```
    cd /tmp/  
    psql -d gwells -U <user>  -f ./database/scripts/truncate-search-ready-data.sql
    ```
