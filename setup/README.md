# Groundwater Wells

## Local development

To run this project in your development machine, ensure that Git, Python 3.5 and PostgreSQL 9.5 is installed. When installing Python, ensure 'install for everyone' and 'PATH' options are enabled. Ensure you run all shell windows in ADMIN mode. Follow these steps:

##### Preemptive TL;DR

OS X:

```
./setup_osx.sh
```


##### Setup

1.  Prerequisites:

    * [Git](https://git-scm.com/downloads/)
    * [Python 3.5](https://www.python.org/downloads/)
    * [PostgreSQL 9.5](https://www.postgresql.org/download/)
    * [VirtualEnv](https://virtualenv.pypa.io/)
    * [VirtualEnvWrapper (OS X)](http://virtualenvwrapper.readthedocs.org/)
    * [VirtualEnvWrapper-Win (Windows)](https://pypi.python.org/pypi/virtualenvwrapper-win/)

    </p>

    OS X: Install packages with Brew and Pip3

    ```
    /usr/bin/ruby -e "$( curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install )"
    brew install git postgresql python3
    pip3 install postgresql virtualenv virtualenvwrapper --user
    ```

    Windows: Install virtualenvwrapper-win instead of virtualenvwrapper.

    ```
    pip3 install virtualenvwrapper-win
    ```

2.  GitHub

    Fork this repo and clone it.

    ```
    git clone https://github.com/<github-user>/gwells.git
    ```

    Change directory to repo, then add remote (upstream) origin.

    ```
    cd gwells
    git remote add upstream https://github.com/bcgov/gwells.git
    ```

    Set email address and name
    ```
    git config --global user.email <GitHub registered email address>
    git config --global user.name <GitHub registered firstName LastName>
    ```

    Set push default and line endings (Linux LF, not Win CRLF)
    ```
    git config --global push.default simple
    git config --global core.autocrlf input
    ```

3.  PostgreSQL

    Use the psql command line tool to create a database user and empty database.

    ```
    psql -U postgres -c "CREATE USER gwells WITH createdb;"
    psql -U postgres -c "CREATE DATABASE gwells WITH OWNER='gwells';"
    ```

    PostgreSQL may need to be configured.  OS X file locations are used here.

    ```
    brew services start postgresql
    initdb /usr/local/var/postgres/
    /usr/local/Cellar/postgresql/<version-number>/bin/createuser -s postgres
    ```

4.  Virtual Environment

    Using VirtualEnvWrapper create a virtual environment.

    ```
    mkvirtualenv gwells
    ```

    Work within your virtual environment.
    ```
    workon gwells
    ```

5.  Config variables

    If you are developing against a Postgres database you can set environment variables with a postactivate script.

    Windows: Add the following to %USERPROFILE%\Envs\myenv\Scripts\activate.bat.

    ```
    SET DATABASE_SERVICE_NAME=postgresql
    SET DATABASE_ENGINE=postgresql
    SET DATABASE_NAME=gwells
    SET DATABASE_USER=gwells
    SET DATABASE_PASSWORD=gwells
    SET DATABASE_SCHEMA=public
    SET DJANGO_DEBUG=True
    SET APP_CONTEXT_ROOT=gwells
    SET ENABLE_GOOGLE_ANALYTICS=False
    SET ENABLE_DATA_ENTRY=True
    SET BASEURL=http://gwells-dev.pathfinder.gov.bc.ca/
    ```

    OS X: Export runtime variables at the command line.
    ```
    export DATABASE_SERVICE_NAME=postgresql
    export DATABASE_ENGINE=postgresql
    export DATABASE_NAME=gwells
    export DATABASE_USER=gwells
    export DATABASE_PASSWORD=gwells
    export DATABASE_SCHEMA=public
    export DJANGO_DEBUG=True
    export APP_CONTEXT_ROOT=gwells
    export ENABLE_GOOGLE_ANALYTICS=False
    export ENABLE_DATA_ENTRY=True
    export BASEURL=http://gwells-dev.pathfinder.gov.bc.ca/
    ```

6.  Requirements

    Install requirements (file in root of repo)

    ```
    pip3 install -U -r ../requirements.txt
    ```

7.  Create a development database. You may first have to assign the gwells user a password.

    ```
    python3 ../manage.py migrate
    ```

8.  Start the Django development server.

    ```
    python3 ../manage.py runserver
    ```

9.  Browse to http://127.0.0.1:8000/gwells, the welcome page.


## Deploying to OpenShift

See the [README](https://github.com/bcgov/gwells/blob/master/openshift/templates/README.md) in https://github.com/bcgov/gwells/tree/master/openshift/templates.


#### Logs

By default your Django application is served with gunicorn and configured to output its access log to stderr.
You can look at the combined stdout and stderr of a given pod with this command:

    oc get pods         # list all pods in your project
    oc logs <pod-name>

This can be useful to observe the correct functioning of your application.

#### Special environment variables
Note that environment variables are case sensitive.

#### APP_CONFIG
You can fine tune the gunicorn configuration through the environment variable `APP_CONFIG` that, when set, should point to a config file as documented [here](http://docs.gunicorn.org/en/latest/settings.html).

#### DB_REPLICATE
Until legacy WELLS is shutdown and all works done on GWELLS, there is a nightly replication of WELLS records to GWELLS Production.   This [variable](database/README.md#32) controls the behavior during deploys (to DEV/TEST/PROD) and is one of None, Subset, or Full.  

* Recommended value on DEV:  `Subset` (otherwise the Functional Tests will fail)  
* Recommended value on TEST: `Subset` or `Full`  
* Recommended value on PROD: `Full`  

#### MINIO_ACCESS_KEY
Access key acting as a user ID that uniquely identifies the account.  Set as part of `gwells-minio` deployment but then used in `gwells` deployment to connect to the internal (private) Minio Server.

#### MINIO_SECRET_KEY
Secret key acting as the password to the account.  Set as part of `gwells-minio` deployment but then used in `gwells` deployment to connect to the internal (private) Minio Server.

See our [Wiki page](https://github.com/bcgov/gwells/wiki/Storage-of-Related-Documents) for more details.

#### S3_HOST
Endpoint to the public S3 Server (e.g. `s3.ca-central-1.amazonaws.com`)

#### S3_ROOT_BUCKET
Top-level S3 bucket that organizes all publicly viewable documentes (e.g. `gwells-docs`)

#### DJANGO_SECRET_KEY
When using one of the templates provided in this repository, this environment variable has its value automatically generated. For security purposes, make sure to set this to a random string as documented [here](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SECRET_KEY).

#### DJANGO_DEBUG
Set to `True` to enable debugging.  Recommended value:  `True`

NOTE: On local developer environments, the `gradlew` tests will fail with `DJANGO_DEBUG=False` unless the developer manually runs `python3 manage.py collectstatic`.

#### ENABLE_DATA_ENTRY  
Set to `True` to enable debugging.  Recommended value:  Not set for Production (as the feature is not released); `True` for Development.

#### ENABLE_GOOGLE_ANALYTICS
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
