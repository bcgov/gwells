# Aquifers app

## Django app under the `gwells` project

This is a distinct app under the GWELLS project, created using the Django command:
`python manage.py startapp aquifers`, and included under this entry in the [settings.py](../gwells/settings/__init__.py#L102) file.  Sub-folders follow the standard Django setup.

## Test data fixture

To facilitate the CodeWithUs effort, we have a sample set of data available in a
[aquifers-sample file](./fixtures/aquifers-sample.json).  It is a subset of the full dataset, and has been sanitized (personal names have been deleted; in fact the entire registries_persons table is not inclued).

'''
python manage.py loaddata aquifers-sample.json 
'''

Output from the above command should be:
```
Installed 35299 object(s) from 1 fixture(s)
```

The following database tables should have these number of rows:
```
psql -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER

gwells=> select count(*) from well;
 count 
-------
  1010
(1 row)

gwells=> select count(*) from hydraulic_property ;
 count 
-------
    60
(1 row)

gwells=> select count(*) from aquifer;
 count 
-------
  1195
(1 row)
```


