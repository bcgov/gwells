# Database Scripts

## Replicate from the legacy Oracle database

GWELLS uses the PostgreSQL extension oracle-fdw [oracle-fdw](https://github.com/laurenz/oracle_fdw) to read from the
legacy database (WELLS schema of ENVPROD1.NRS.GOV.BC.CA).

Static code tables are maintained in this [GitHub](../code-tables) repo, while dynamic data is replicated.  There are two stored procedures that support this.

1. `gwells_setup_replicate()`
- owned by GWELLS user
- clears all data tables
- prepares the ETL table 
- can be run by GWELLS user or PostgreSQL administrator (e.g. psql -d gwells -U userGN0 -c 'select gwells_setup_replicate();')

2. `gwells_replicate()`
- owned by GWELLS user
- "COPY" into static code tables from GitHub repo
- INSERT into dynamic data tables from Oracle FDW
- INSERT into the main "wells" PostgreSQL table from the local ETL table
- must be run by PostgreSQL administrator, due to restricted COPY command (e.g. psql -d gwells -c 'select gwells_replicate();')

The logged output includes the number of rows inserted into the main "wells" PostgreSQL database table

```ssh-4.2$ psql -d gwells -c 'select gwells_replicate();' 
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
NOTICE:  ... 111710 rows loaded into the main "wells" table
NOTICE:  Finished gwells_replicate() procedure.
 gwells_replicate 
------------------
 
(1 row)
```
