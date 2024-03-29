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

## OpenShift Health Checks
Resetting the database is this manner will interfere with the health checks, which report that the application server is unresponsive and then immediately roll back to the previous image (which has the obsolete /migrations/000n_xxx files).

To work around this, 'pause' the deployment for the specific environment; for example, moe-gwells-dev is paused by clicking on the 'Actions' dropdown button at the top right of the Deployment [page](https://console.pathfinder.gov.bc.ca:8443/console/project/moe-gwells-dev/browse/dc/gwells?tab=history).  

NOTE: Do not scale down the pod to 0, as this will not allow the pipline to deploy the reset migration  files to the pod.

Once the deployment has finished, unpause the deployment and then the pod will deploy with the updated /migrations/000n_xxx files, against an 'empty' database.  Remember that the 'python manage.py migrate' step is configured in the Post-Commit Hook of the [build configuration](https://console.pathfinder.gov.bc.ca:8443/console/project/moe-gwells-tools/edit/builds/gwells-developer).


# Integration with Django Administrator account

## OpenShift Secrets
The administrator account details are recorded as an OpenShift Secret (i.e. PROD environment as the secret here under the umbrella gwells-django [secret](https://console.pathfinder.gov.bc.ca:8443/console/project/moe-gwells-prod/browse/secrets/gwells-django) ).


Currently, these values are used as part of the automatic step to create the admin account:
`python manage.py post-deploy`

This is currently in the ./scripts/gwells-deploy.sh script and called in the mid-lifecycle hook; this will be moved into the Pipeline, at the appropriate Stage.
