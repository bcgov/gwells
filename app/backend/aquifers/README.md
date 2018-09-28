# Aquifers app

## Django app under the `gwells` project

This is a distinct app under the GWELLS project, created using the Django command:
`python manage.py startapp aquifers`, and included under this entry in the [settings.py](../gwells/settings/__init__.py#L102) file.  Sub-folders follow the standard Django setup.

## Test data fixture

To facilitate the CodeWithUs effort, we have a sample set of data available in a
[aquifers-sample file](./fixtures/aquifers-sample.json).  It is a subset of the full dataset, referencing
only the wells that are in the test data fixture).

It is automatically loaded in DEV and TEST, as part of the Jenkinsfile.  It is NOT loaded in PROD.

