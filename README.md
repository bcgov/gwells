# Groundwater Wells and Aquifers (GWELLS)

## Table of Contents

1. [Introduction](#introduction)
1. [Developing GWELLS](#developing-gwells)
    * [Running the GWELLS application locally](#Running-the-GWELLS-application-locally)
    * [Authentication](#Authentication)
    * [Running tests](#Running-tests)
1. [Architecture](#Architecture)
1. [Contributing](#contributing)
    * [Code With Us](#code-with-us)
1. [Issues](#issues)
1. [License](#license)

## Introduction

The Ministry of Environment receives and processes groundwater data and information related to the construction, alteration and decommissioning of groundwater wells. Well construction and reporting requirements are regulated under the Water Sustainability Act and Groundwater Protection Regulation. The information collected and stored is used by government and other users to help inform decisions related to the management of the groundwater resource in B.C.

GWELLS, the new groundwater data repository, aims to improve the user experience when submitting and searching for well information, to improve the quality of the data being submitted, and to improve the overall functionality of the system to meet user and regulatory requirements.

The application is being developed as an open source solution.

## Developing GWELLS

### Running the GWELLS application locally

[Clone the GWELLS repository](https://help.github.com/en/articles/cloning-a-repository) and run the application with [Docker](https://store.docker.com/search?type=edition&offering=community):
```sh
cd gwells
docker-compose up
```

Visit the following links to browse the API and frontend applications:

* Django REST API development server: http://localhost:8000/gwells/api/
* Vue frontend development server: http://localhost:8080/

### Authentication

Some GWELLS pages (submitting new well reports, adding or editing aquifers, or adding or editing qualified well drillers to the registry) require authentication. Authentication uses the Province's Single Sign-On system. A GWELLS team member can request access for collaborators if needed.

### Running tests:

Django unit tests:
```sh
cd app/backend
python manage.py test
```

Vue unit tests:
```sh
cd app/frontend
npm run unit
```

Postman API tests:
Import the json test collections in the `api-tests/` folder into [Postman](https://www.getpostman.com/).

## Architecture

GWELLS uses PostgreSQL (with PostGIS), Django REST Framework, and Vue.js. We also use both AWS S3 and a self-hosted Minio service for storing documents.

Our production and staging environments run on an OpenShift container platform cluster.  OpenShift templates for services are located in the `openshift/` folder, along with more information about dev and staging environments on our cluster.

![GWELLS container diagram](pics/container_diagram.png)

## Contributing

Government employees, the public and members of the private sector are encouraged to contribute.  Please read and follow our [Code of Conduct](https://github.com/bcgov/gwells/blob/master/CODE_OF_CONDUCT.md).

All contributors retain original copyright, but are granting a world-wide, royalty-free, perpetual, irrevocable, non-exclusive, transferable license to all users.  This project is covered by an [Apache v2.0 license](https://github.com/bcgov/gwells/blob/master/LICENSE).

### Code With Us

GWELLS has received significant contributions from the developer community through the [BC Dev Exchange](https://bcdevexchange.org/) Code With Us program, where paid opportunities to build features for GWELLS and other applications are posted regularly.

## Issues
Issues are tracked on the [GWELLS Trello board](https://trello.com/b/2UQZgXHR/wells-project-board).

## License

Code released under the [Apache License, Version 2.0](https://github.com/bcgov/gwells/blob/master/LICENSE).
