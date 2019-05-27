# Groundwater Wells and Aquifers (GWELLS)

## Introduction

The Ministry of Environment receives and processes groundwater data and information related to the construction, alteration and decommissioning of groundwater wells. Well construction and reporting requirements are regulated under the Water Sustainability Act and Groundwater Protection Regulation. The information collected and stored is used by government and other users to help inform decisions related to the management of the groundwater resource in B.C.

GWELLS is the new groundwater data repository and is intended to replace the current WELLS system. GWELLS aims to improve the user experience when submitting and searching for well information, to improve the quality of the data being submitted, and to improve the overall functionality of the system to meet user and regulatory requirements.

The application is being developed as an open source solution.

## Developing GWELLS

### Prerequisites

* [Docker Community Edition (signup  required)](https://store.docker.com/search?type=edition&offering=community)

* [git](https://git-scm.com/downloads)

### Running the GWELLS application locally

Run the GWELLS application with docker-compose:
```sh
cd gwells
docker-compose up
```

Visit the following links to browse the API and frontend applications:

* Django REST API development server: http://localhost:8000/gwells/api/
* Vue frontend development server: http://localhost:8080/

### Running tests:

Django unit tests:
```sh
cd app/backend
python manage.py test
```

Vue unit tests:
```sh
cd app/frontend
npm run test:unit
```

Postman API tests:
Import the json test collections in the `api-tests/` folder into [Postman](https://www.getpostman.com/).

### Import a Shapefile

Single shapefile, with aquifer ID specified in CLI.
```
docker-compose exec backend python manage.py import_shapefile 2 aquifers/fixtures/shp/shapefile.zip
```

Bulk import, requires the AQ_NUMBER attribute on each polygon. Requires a folder with shapefiles to be prepared and passed in (zipped or not). Note: if DEBUG=True, all geometries will be uploaded to a random aquifer instead of the one matching its' number, so we can test locally with a development database.
```
mkdir app/backend/bulk
mv DATABC_EXPORT_FILE.zip app/backend/bulk/

docker-compose exec backend python manage.py import_bulk_shapefile bulk
```

### Importing Licences

To download new licence data from DataBC and merge it into your DB, do ```
docker-compose exec backend python manage.py import_licences
```

## Contributing

Please see [CONTRIBUTING.md](https://github.com/bcgov/gwells/blob/master/CONTRIBUTING.md)

## Issues
Issues are tracked on the [GWELLS Trello board](https://trello.com/b/2UQZgXHR/wells-project-board).

## Architecture

GWELLS is built with PostgreSQL (with PostGIS), Django REST Framework, and Vue.js, and the production application runs on an OpenShift cluster.  OpenShift templates for services are located in the `openshift/` folder.

![GWELLS container diagram](pics/container_diagram.png)

## License

Code released under the [Apache License, Version 2.0](https://github.com/bcgov/gwells/blob/master/LICENSE).
