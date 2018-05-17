# Integration with Django Migrations

## Django Object-Relational Mapping (ORM)
Django stores an object-oriented via of the persistent data, for example the [Registries](https://github.com/bcgov/gwells/blob/developer/registries/models.py) component of GWELLS.  As the object-oriented model is updated and refined, changes are queued as a incremental updates that will be applied to the back-end database.  The mechanism is via text files that are run in order (i.e. again [Registries](https://github.com/bcgov/gwells/tree/developer/registries/migrations) as an example).  This list of files will grow as updates are made to the object-oriented model.

## Database Metadata
The database has several metadata tables that record the current 'state' of the database structures (in relation to the Django 'state' stored in the ORM and migration files), specifically the django_migrations table, for example:
```
gwells=> select * from django_migrations;
 id |     app      |                   name                  
----+--------------+-----------------------------------------
  1 | contenttypes | 0001_initial                            
  2 | auth         | 0001_initial                            
  3 | admin        | 0001_initial                            
  4 | admin        | 0002_logentry_remove_auto_add           
  5 | contenttypes | 0002_remove_content_type_name           
  6 | auth         | 0002_alter_permission_name_max_length   
  7 | auth         | 0003_alter_user_email_max_length        
  8 | auth         | 0004_alter_user_username_opts           
  9 | auth         | 0005_alter_user_last_login_null         
 10 | auth         | 0006_require_contenttypes_0002          
 11 | auth         | 0007_alter_validators_add_error_messages
 12 | auth         | 0008_alter_user_username_max_length     
 13 | gwells       | 0001_initial                            
 14 | registries   | 0001_initial                            
 15 | sessions     | 0001_initial                            
(15 rows)
```

Major changes (e.g. to the User model, or Authentication, or to deletion/renaming of database objects) are not well handled in Django.  In this situation, it is better to 'reset' all the migrations (see [article](https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html)).

## Reset django_migrations table
We reset ALL the database objects currently, as we are still in the 'replicate from legacy system' mode with no new data.  Until we start entering production data (e.g. Registries) we can reset the target database (DEV, or TEST or PROD) by running [reset-gwells-all.sh](../../scripts/reset-gwells-all.sh).

It's better to run the reset script on the postgresql pod, as the gwells pod will be brought down as part the 'Recreate' strategy of the rollout.

## OpenShift Health Checks
Resetting the database is this manner will interfere with the health checks, which report that the application server is unresponsive and then immediately roll back to the previous image (which has the obsolete /migrations/000n_xxx files).

To work around this, 'pause' the deployment for the specific environment; for example, moe-gwells-dev is paused by clicking on the 'Actions' dropdown button at the top right of the Deployment [page](https://console.pathfinder.gov.bc.ca:8443/console/project/moe-gwells-dev/browse/dc/gwells?tab=history).  

NOTE: Do not scale down the pod to 0, as this will not allow the pipline to deploy the reset migration  files to the pod.

Once the deployment has finished, unpause the deployment and then the pod will deploy with the updated /migrations/000n_xxx files, against an 'empty' database.  Remember that the 'python manage.py migrate' step is configured in the Post-Commit Hook of the [build configuration](https://console.pathfinder.gov.bc.ca:8443/console/project/moe-gwells-tools/edit/builds/gwells-developer).



## Replicate from the legacy Oracle database

GWELLS uses the PostgreSQL extension [oracle-fdw](https://github.com/laurenz/oracle_fdw) to read from the
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

Static code tables are maintained in this [GitHub](../../../tree/master/database/codetables) repo, while dynamic data is replicated.  There are a stored DB procedures that acts as a 'driver' scripts `db_replicate_step1(boolean)` and `db_replicate_step2()` that run the replication:


There is also a SQL script `data-load-static-codes.sql`
- "COPY" into static code tables from deployed CSV files
- run on the gwells pod (which has all CSV files under `$VIRTUAL_ENV/src/database/codetables/`)


The replicate process can be run ad-hoc on the PostgreSQL pod or on a local developer workstation, passing a parameter to the stored procedure.

`true` : Only a subset of data (i.e. `AND wells.well_tag_number between 100001 and 113567`)
`false`: Full data replication


The logged output includes the number of rows inserted into the main "wells" PostgreSQL database table

```
ssh-4.2$ psql -t -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c 'SELECT db_replicate_step1(_subset_ind=>false);'
ssh-4.2$ psql -t -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c 'SELECT db_replicate_step2 ();'
```

# Integration with Django Administrator account

## OpenShift Secrets
The administrator account details are recorded as an OpenShift Secret (i.e. PROD environment as the secret here under the umbrella gwells-django [secret](https://console.pathfinder.gov.bc.ca:8443/console/project/moe-gwells-prod/browse/secrets/gwells-django) ).


Currently, these values are used as part of the manual step to create the admin account, by logging onto the gwells pod:
```
(app-root)sh-4.2$ python manage.py createsuperuser
REQUIRE_ENV_VARIABLES is set to False
Username: admin
Email address: xxx@gov.bc.ca
Password: <paste-in-password-from-openshift-secret>
Password (again): <paste-in-password-from-openshift-secret>
Superuser created successfully.
```

This opaque secret also records the obfuscated administration screen URL (under `admin_url`).  Each environment (gwells-moe-dev, gwells-moe-test, gwells-moe-prod) has its own values in this secret.


