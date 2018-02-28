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

Static code tables are maintained in this [GitHub](../../../tree/master/database/code-tables) repo, while dynamic data is replicated.  There are a stored DB procedures that acts as a 'driver' script [full_db_replication.sql](scripts/db_replicate.sql) that run several stored procedures:

There is also a SQL script `data-load-static-codes.sql`
- "COPY" into static code tables from deployed CSV files  
- run on the gwells pod (which has all CSV files under `$VIRTUAL_ENV/src/database/code-tables/`)


The replicate process can be run ad-hoc on the PostgreSQL pod or on a local developer workstation, passing a parameter to the stored procedure.  

`true` : Only a subset of data (i.e. `AND wells.well_tag_number between 100001 and 113567`)  
`false`: Full data replication  


The logged output includes the number of rows inserted into the main "wells" PostgreSQL database table

```
ssh-4.2$ psql -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c 'SELECT db_replicate(false);'
NOTICE:  Starting populate_xform() procedure...
NOTICE:  table "xform_well" does not exist, skipping
NOTICE:  Created xform_well ETL table
NOTICE:  ... transforming wells data (= ACCEPTED) via xform_well ETL table...
NOTICE:  ... 111350 rows loaded into the xform_well table
...
NOTICE:  ... importing xform into the well table
NOTICE:  ...xform data imported into the well table
NOTICE:  111350 rows loaded into the well table
...
```
