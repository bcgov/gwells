# Registries app

## Django app under the `gwells` project

This is a distinct app under the GWELLS project, created using the Django command:
`python manage.py startapp registries`, and included under this entry in the [settings.py](../gwells/settings/__init__.py#L102) file.  Sub-folders follow the standard Django setup.

NOTE: Related files are under the gwells project folder, with the other files but in the a `registries` subfolder:
- [app/database/codetables/registries/](../app/database/codetables/registries/)
- [app.database/scripts/registries/](../app/database/scripts/registries/)

Please note that there is a dependency on the ProvinceStateCode model of gwells, so any exports of registries will need this as well, for example:
```
python manage.py dumpdata registries gwells.ProvinceStateCode
```
