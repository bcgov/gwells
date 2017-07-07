# Database Scripts

## Export from the legacy Oracle database

The legacy database is WELLS schema of ENVPROD1.NRS.GOV.BC.CA, and was exported using SQL Developer (via [Citrix](https://dts.gov.bc.ca/Citrix/BCGOVWeb/) *Kamloops Desktop - ArcGIS 10-2* desktop).  The transformation of data (e.g. datatype conversion, lookup code foreign keys, concatentation of strings) is done as part of the export script:
    [xform-submission-data.sql](scripts/sql-developer/xform-submission-ready-data.sql)

2. From the Windows Start Menu on the lower left of the Windows TaskBar, open Oracle SQL*Developer:
```-> All Programs -> Oracle Tools -> Oracle SQL Developer```

3. Login to ENVPROD1.NRS.GOV.BC.CA with an Oracle DB Account that can view WELLS schema objects

4.  Navigate to the Oracle SQL Developer WorkSheet tab and enter the path of the transformation script, via GitHub:
    `@https://cdn.rawgit.com/bcgov/gwells/master/database/scripts/sql-developer/xform-submission-ready-data.sql`

    *NOTE*: If Citirx permissions prevent you from running this script directly (i.e. unable to open file), then either
    copy/download the script to a file on the Citrix account.  Do not copy-and-paste as the run script "@" syntax is 
    required to filter out the "SELECT FROM ... " output from the CSV.

    Four CSV files will be created on your networked Home drive (H:\), prefixed with 'xform' to denote that an additional transformation step is required before inserting into 'gwells' tables:
    ```H:\xform_gwells_land_district.csv    
    H:\xform_gwells_well.csv
    H:\xform_gwells_driller.csv
    H:\xform_gwells_drilling_company.csv```

5. Copy the CSV files over to your local workstation (e.g. ~/projects/gwells/legacy-data/postgres) , ready to be included in the
    `rsync` [step below](#rsync-csv).  SQL Developer insists on adding a blank line at the end of each generated CSV file, which
    runs into a PostGres bug when importing CSV with such a blank line.   Remove this last line from each of the genereated files, either manually or via sed/awk/perl etc.

   *NOTE*: The [code tables](code-tables) are not derived from the legacy tables, so they are prefixed
   with the 'gwells' to denote this.  The rows, and UUID identifiers, are pre-populated and ready to be loaded:
    ```gwells_bedrock_material.csv
    gwells_bedrock_material_descriptor.csv
    gwells_drilling_method.csv
    gwells_ground_elevation_method.csv
    gwells_intended_water_use.csv
    gwells_lithology_colour.csv
    gwells_lithology_hardness.csv
    gwells_lithology_moisture.csv
    gwells_lithology_structure.csv
    gwells_lithology_weathering.csv
    gwells_province_state.csv
    gwells_surficial_material.csv
    gwells_well_activity_type.csv
    gwells_well_class.csv
    gwells_well_subclass.csv
    gwells_well_yield_unit.csv```    

## Loading data upon which to run a Search (against the PostGres DB) 

The legacy data was exported into human-readable CSV files, and stored outside of GitHub.  This is for both 
security and storage reasons.  The seqreset.sql script was generated via Django using:
    `python manage.py sqlsequencereset gwells > ./database/scripts/seqreset.sql`

Consolidate all scripts and CSV files into a single folder on the developer workstation.  For example:
```cp -v ~/projects/gwells/github/database/scripts/*.sql /Users/garywong/tmp/gwells
cp -v ~/projects/gwells/github/database/code-tables/*.csv  /Users/garywong/tmp/gwells
```

    The complete file listing is:
    - gwells_drilling_method.csv
    - gwells_ground_elevation_method.csv
    - gwells_intended_water_use.csv
    - gwells_province_state.csv
    - gwells_well_activity_type.csv
    - gwells_well_class.csv
    - gwells_well_subclass.csv
    - gwells_well_yield_unit.csv
    - load-submission-ready-data.sql
    - truncate-submission-ready-data.sql
    - xform_gwells_driller.csv*
    - xform_gwells_drilling_company.csv
    - xform_gwells_land_district.csv
    - xform_gwells_well.csv

1.  Sync all CSV and SQL files to Postgres pod, from that single source directory <a id="rsync-csv"></a> on the developer workstation:
```oc rsync /Users/garywong/tmp/gwells postgresql-3-zxo8x:/tmp```

2.  Remote into Postgres pod (from developer workstation).  Note that the the pod name changew with
each pod deployment, so get the name first (i.e. *oc get pods*) from the correct project (dev/test/prod):
```oc rsh postgresql-3-zxo8x```

3.  Once in the the remote shell:
    ```cd /tmp/gwells  
    psql -d gwells -U <user>  -f ./truncate-submission-ready-data.sql
    psql -d gwells -U <user>  -f ./load-submission-ready-data.sql
    psql -d gwells -U <user>  -f ./seqreset.sql```

4. Run the psql client to verify the database objects:
```psql -d gwells -U <user>```

## Clear all data from which the live Search ran

Repeat steps 1-3, and then:

4.  From the remote shell into the Postgres pod:
```cd /tmp/  
psql -d gwells -U <user>  -f ./database/scripts/truncate-submission-ready-data.sql
```
