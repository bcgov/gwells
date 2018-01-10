# Database Scripts

## Replicate from the legacy Oracle database

GWELLS uses the PostgreSQL extension oracle-fdw [oracle-fdw](https://github.com/laurenz/oracle_fdw) to read from the
legacy database (WELLS schema of ENVPROD1.NRS.GOV.BC.CA).  This oracle-fdw extensions connect to the legacy Oracle Database via Environment Variables defined in the [OpenShift Web Console](https://console.pathfinder.gov.bc.ca:8443/console/):  
-- Applications > Deployments  
--- postgresql  
---- Environment   

<table>   
<tr><td>Name</td><td>Value</td></tr>
<tr><td>FDW_USER</td><td>proxy_wells_gwells</td></tr>
<tr><td>FDW_PASS</td><td><i>password</i></td></tr>
<tr><td>FDW_FOREIGN_SCHEMA</td><td>WELLS</td></tr>
<tr><td>FDW_NAME</td><td>wells_oradb</td></tr>
<tr><td>FDW_SCHEMA</td><td>wells</td></tr>
<tr><td>FDW_FOREIGN_SERVER</td><td>//nrk1-scan.bcgov/envprod1.nrs.bcgov</td></tr>
</table>    

The image automatic re-deploys if any Environment Variable values are updated, but the oracle-fdw FDW_ * details do NOT get recreated
unless the lock file is deleted first from the pod (i.e. `rm /var/lib/pgsql/data/userdata/fdw.conf`).

Note that environment variables are also used for the PostgreSQL database connection:
<table>   
<tr><td>Name</td><td>Value</td></tr>
<tr><td>POSTGRESQL_USER</td><td><i>username</i></td></tr>
<tr><td>POSTGRESQL_PASSWORD</td><td><i>password</i></td></tr>
<tr><td>POSTGRESQL_DATABASE</td><td>gwells</td></tr>
</table>    

The data replication is controlled by the environment variable<table>   
<tr><td>Name</td><td>Value</td></tr>
<tr><td>DB_REPLICATE</td><td><i>None | Subset | Full</i></td></tr>
</table>    

`None`  : No replication  
`Subset`: Only a subset of data (i.e. `AND wells.well_tag_number between 100001 and 113567`)  
`Full`  : Full data replication  

Static code tables are maintained in this [GitHub](../../../tree/master/database/code-tables) repo, while dynamic data is replicated.  There are a stored DB procedures that acts as a 'driver' script [full_db_replication.sql](scripts/full_db_replication.sql) that runs these stored procedures:

```
PERFORM gwells_populate_xform(false);  
PERFORM gwells_populate_well();   
PERFORM gwells_migrate_screens();  
PERFORM gwells_migrate_production();  
PERFORM gwells_migrate_casings();  
PERFORM gwells_migrate_perforations();  
PERFORM gwells_migrate_aquifers();  
PERFORM gwells_migrate_lithology();  
```

There is also an SQL script `data-load-static-codes.sql`
- "COPY" into static code tables from deployed CSV files  
- run on the gwells pod (which has all CSV files under `$VIRTUAL_ENV/src/database/code-tables/`)

The logged output includes the number of rows inserted into the main "gwells_wells" PostgreSQL database table

```
ssh-4.2$ psql -d gwells -c 'select gwells_replicate();' 
NOTICE:  Starting gwells_replicate() procedure...
NOTICE:  ... importing gwells_intended_water_use code table
NOTICE:  ... importing gwells_well_class code table
NOTICE:  ... importing gwells_well_subclass code table
NOTICE:  ... importing gwells_province_state code table
NOTICE:  ... importing gwells_well_yield_unit code table
NOTICE:  ... importing gwells_drilling_method code table
NOTICE:  ... importing gwells_ground_elevation_method code table
NOTICE:  ... importing gwells_land_district data table
NOTICE:  ... transforming wells data (!= REJECTED) via xform_gwells_well ETL table...
NOTICE:  ... importing ETL into the main "wells" table
NOTICE:  ... *111710* rows loaded into the main "wells" table
NOTICE:  Finished gwells_replicate() procedure.
 gwells_replicate 
------------------
 
(1 row)
```
