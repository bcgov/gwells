[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/gate?key=org.sonarqube:bcgov-gwells)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard?id=org.sonarqube%3Abcgov-gwells) [![Coverage](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=coverage&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)


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
└── code-tables     - Static code table sql scripts
└── cron            - Shell scripts
└── scripts         - PostgrSQL psql scripts
  └── sql-developer - SQL Developer Oracle SQL scripts

openshift/          - OpenShift-specific files
├── scripts         - helper scripts
└── templates       - application templates

requirements.txt    - list of dependencies

```

## Local development

To run this project in your development machine, ensure that Git, Python 3.5 and PostgreSQL 9.5 is installed. When installing Python, ensure 'install for everyone' and 'PATH' options are enabled. Ensure you run all shell windows in ADMIN mode. Follow these steps:

1. Use the psql command line tool to create a database user and empty database.

    ```
    psql -U postgres
    
    create user gwells with createdb;
    create database gwells with owner=gwells;
    ```

2. Create and activate a [virtualenv](https://virtualenv.pypa.io/) (you may want to use [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/)).

    If working on Windows install virtualenvwrapper-win via pip.
    
    `pip install virtualenvwrapper-win`

    Create a virtual environment.

    `mkvirtualenv gwells`

    Work within your virtual environment.
    
    `workon gwells`

    If you are developing against a Postgres database you can set environment variables with a postactivate script.
    When using virtualenvwrapper-win find the activate.bat script located in %USERPROFILE%\Envs\myenv\Scripts and add the following:

    ```
    SET DATABASE_SERVICE_NAME=postgresql
    SET DATABASE_ENGINE=postgresql
    SET DATABASE_NAME=<dbname>
    SET DATABASE_USER=<user>
    SET DATABASE_PASSWORD=<pw>
    SET DJANGO_DEBUG=True
    SET APP_CONTEXT_ROOT=gwells
    ```

3. Fork this repo and clone your fork:

    `git clone https://github.com/<github-user>/gwells.git`

4. Change directory to gwells (cd gwells), then add remote (upstream) origin:

    `git remote add upstream https://github.com/bcgov/gwells.git`
    
5. Install dependencies:

    `pip install -r requirements.txt`
    
6. Create a development database. You may first have to assign the gwells user a password:

    `python manage.py migrate`

7. If everything is alright, you should be able to start the Django development server:

    `python manage.py runserver`

8. Open your browser and go to http://127.0.0.1:8000/gwells, you will be greeted with a welcome page.


## Deploying to OpenShift

See the [README](https://github.com/bcgov/gwells/blob/master/openshift/templates/README.md) in https://github.com/bcgov/gwells/tree/master/openshift/templates.


## Logs

By default your Django application is served with gunicorn and configured to output its access log to stderr.
You can look at the combined stdout and stderr of a given pod with this command:

    oc get pods         # list all pods in your project
    oc logs <pod-name>

This can be useful to observe the correct functioning of your application.

## Special environment variables
Note that environment variables are case sensitive.

### APP_CONFIG
You can fine tune the gunicorn configuration through the environment variable `APP_CONFIG` that, when set, should point to a config file as documented [here](http://docs.gunicorn.org/en/latest/settings.html).

### DB_REPLICATE 
Until legacy WELLS is shutdown and all works done on GWELLS, there is a nightly replication of WELLS records to GWELLS Production.   This [variable](database/README.md#32) controls the behavior during deploys (to DEV/TEST/PROD) and is one of None, Subset, or Full.  

* Recommended value on DEV:  `Subset` (otherwise the Functional Tests will fail)  
* Recommended value on TEST: `Subset` or `Full`  
* Recommended value on PROD: `Full`  

### MINIO_ACCESS_KEY 
Access key acting as a user ID that uniquely identifies the account.  Set as part of `gwells-minio` deployment but then used in `gwells` deployment to connect to the internal (private) Minio Server.

### MINIO_SECRET_KEY 
Secret key acting as the password to the account.  Set as part of `gwells-minio` deployment but then used in `gwells` deployment to connect to the internal (private) Minio Server.

See our [Wiki page](https://github.com/bcgov/gwells/wiki/Storage-of-Related-Documents) for more details.

### S3_HOST 
Endpoint to the public S3 Server (e.g. `s3.ca-central-1.amazonaws.com`)

### S3_ROOT_BUCKET 
Top-level S3 bucket that organizes all publicly viewable documentes (e.g. `gwells-docs`)

### DJANGO_SECRET_KEY
When using one of the templates provided in this repository, this environment variable has its value automatically generated. For security purposes, make sure to set this to a random string as documented [here](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SECRET_KEY).

### DJANGO_DEBUG 
Set to `True` to enable debugging.  Recommended value:  `True`

NOTE: On local developer environments, the `gradlew` tests will fail with `DJANGO_DEBUG=False` unless the developer manually runs `python manage.py collectstatic`.

### ENABLE_DATA_ENTRY  
Set to `True` to enable debugging.  Recommended value:  Not set for Production (as the feature is not released); `True` for Development.

### ENABLE_GOOGLE_ANALYTICS
Set to `True` to enable Google Analytics.  Recommended value:  Not set for Development; `True` for Production.

## One-off command execution
At times you might want to manually execute some command in the context of a running application in OpenShift.
You can drop into a Python shell for debugging, create a new user for the Django Admin interface, or perform any other task.

You can do all that by using regular CLI commands from OpenShift.
To make it a little more convenient, you can use the script `openshift/scripts/run-in-container.sh` that wraps some calls to `oc`.
In the future, the `oc` CLI tool might incorporate changes
that make this script obsolete.

Here is how you would run a command in a pod specified by label:

1. Inspect the output of the command below to find the name of a pod that matches a given label:

        oc get pods -l <your-label-selector>

2. Open a shell in the pod of your choice. Because of how the images produced
  with CentOS and RHEL work currently, we need to wrap commands with `bash` to
  enable any Software Collections that may be used (done automatically inside
  every bash shell).

        oc exec -p <pod-name> -it -- bash

3. Finally, execute any command that you need and exit the shell.

Related GitHub issues:
1. https://github.com/GoogleCloudPlatform/kubernetes/issues/8876
2. https://github.com/openshift/origin/issues/2001


The wrapper script combines the steps above into one. You can use it like this:

    ./run-in-container.sh ./manage.py migrate          # manually migrate the database
                                                       # (done for you as part of the deployment process)
    ./run-in-container.sh ./manage.py createsuperuser  # create a user to access Django Admin
    ./run-in-container.sh ./manage.py shell            # open a Python shell in the context of your app

If your Django pods are labeled with a name other than "django", you can use:

    POD_NAME=name ./run-in-container.sh ./manage.py check

If there is more than one replica, you can also specify a POD by index:

    POD_INDEX=1 ./run-in-container.sh ./manage.py shell

Or both together:

    POD_NAME=django-example POD_INDEX=2 ./run-in-container.sh ./manage.py shell


## License

Code released under the [Apache License, Version 2.0](https://github.com/bcgov/gwells/blob/master/LICENSE).
