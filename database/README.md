# Database Scripts

## Export from the legacy Oracle database

The legacy database is WELLS schema of ENVPROD1.NRS.GOV.BC.CA, and was exported using SQL Developer (via [Citrix](https://dts.gov.bc.ca/Citrix/BCGOVWeb/) *Kamloops Desktop - ArcGIS 10-2* desktop).  The transformation of data (e.g. datatype conversion, lookup code foreign keys, concatentation of strings) is done as part of the export script:
    [xform-legacy-data.sql](scripts/sql-developer/xform-legacy-data.sql)

2. From the Windows Start Menu on the lower left of the Windows TaskBar, open Oracle SQL*Developer:
    ```
     -> All Programs -> Oracle Tools -> Oracle SQL Developer
     ```

3. Login to ENVPROD1.NRS.GOV.BC.CA with an Oracle DB Account that can view WELLS schema objects

4.  Navigate to the Oracle SQL Developer WorkSheet tab and enter the path of the transformation script, via GitHub:
    `@https://cdn.rawgit.com/bcgov/gwells/master/database/scripts/sql-developer/xform-legacy-data.sql`

    *NOTE*: If Citirx permissions prevent you from running this script directly (i.e. unable to open file), then either
    copy/download the script to a file on the Citrix account, or simply copy-and-paste into the WorkSheet tab.

    Three CSV files will be created on your networked Home drive (H:\):
    ```
    H:\land_district.csv
    H:\well_owner.csv
    H:\well.csv
    ```

5. Copy the CSV files over to your local workstation, ready to be included in the `rsync` [step below](#rsync-csv).
   
   *NOTE*: The code table values are not derived from the legacy tables.  The rows, and identifiers, are pre-populated and
   ready to be loaded in:
    ```
    province_state.csv
    well_yield_unit.csv
    ```

## Loading data upon which to run a Search (against the PostGres DB) 

The legacy data was exported into human-readable CSV files, and stored outside of GitHub.  This is for both 
security and storage reasons.  The seqreset.sql script was generated via Django using:
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
