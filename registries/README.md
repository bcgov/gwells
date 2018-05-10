# Registries app

## Django app under the `gwells` project

This is a distinct app under the GWELLS project, created using the Django command:
`python manage.py startapp registries`, and included under this entry in the [settings.py](../gwells/settings.py#L76) file:

```
INSTALLED_APPS = (
..    'gwells',
..
```

Sub-folders follow the standard Django setup.
```
-- __pycache__
-- migrations
```

NOTE: Related files are under the gwells project folder, with the other files but in the a `registries` subfolder:
- [database/codetables/registries/](../database/codetables/registries/)
- [database/scripts/registries/](../database/scripts/registries/)

The [post-deploy.sh](../openshift/scripts/post-deploy.sh) step now automatically includes the setup of the registries app code tables and data tables.
```
cd registries/

# @Registries
# Temporary setup of Registries (Well Driller only) as part of Code With Us
# ,including Test Data loaded into the Registries (Driller) tables
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  << EOF
\i clear-tables.sql
\ir ../../scripts/registries/populate-xforms-registries.sql
\i data-load-static-codes.sql
```

Please note that the [populate-registries-from-xform.sql](../database/scripts/registries/populate-registries-from-xform.sql) is *not* automatically called as part of any deployment.  Instead, it is meant to be run locally from the developer's workstation, and that workstation must have the files:
- Registration Action Tracking_Driller.sanitized.csv
- Registry.sanitized.csv
- well_drillers_reg.sanitized.csv

We do not wish these files up on github, so please email the [Architect Owner] (gary.t.wong@gov.bc.ca) if you require them.  Alternatively, request the .json export of the data, using them as fixtures.  

Please note that there is a dependency on the ProvinceStateCode model of gwells, so any exports of registries will need this as well, for example:
```
python manage.py dumpdata registries gwells.ProvinceStateCode
```
