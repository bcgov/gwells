[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/gate?key=org.sonarqube:bcgov-gwells)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard?id=org.sonarqube%3Abcgov-gwells) [![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=coverage&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)



# Groundwater Wells

## Introduction

The Ministry of Environment receives and processes groundwater data and information related to the construction, alteration and decommissioning of groundwater wells and stores that information in the WELLS system. Well construction and reporting requirements are regulated under the Water Sustainability Act and Groundwater Protection Regulation. The information collected and stored in WELLS is used by government and other users to help inform decisions related to the management of the groundwater resource in B.C.

GWELLS is the new groundwater data repository and is intended to replace the current WELLS system. GWELLS aims to improve the user experience when submitting  and searching for well information, to improve the quality of the data being submitted, and to improve the overall functionality of the system to meet user and regulatory requirements.

The application is being developed as an open source solution.

This is a [Django](http://www.djangoproject.com) project based on the [Openshift Django quickstart](https://github.com/openshift/django-ex) that is intended to be deployed on an [OpenShift](https://github.com/openshift/origin) cluster.

It uses the Openshift Source-to-Image (S2I) strategy with Python 3.5 on centos7.  See requirements.txt for Django and dependency versions.


## Special files in this repository

Apart from the regular files created by Django (`project/*`, `welcome/*`, `manage.py`), this repository contains:

```
database/           - Database-specific files
└── codetables     - Static code table sql scripts
└── cron            - Shell scripts
└── scripts         - PostgrSQL psql scripts
  └── sql-developer - SQL Developer Oracle SQL scripts

openshift/          - OpenShift-specific files
├── scripts         - helper scripts
└── templates       - application templates

requirements.txt    - list of dependencies

```

## Development and Deployment

Setup scripts, OpenShift deployment and development details are located in the [setup](./setup/) folder.  Please see the relevant [README.md](../setup/README.md).

## Issues
Issues are tracked on the [GWELLS Trello board](https://trello.com/b/2UQZgXHR/wells-project-board).

## License

Code released under the [Apache License, Version 2.0](https://github.com/bcgov/gwells/blob/master/LICENSE).
