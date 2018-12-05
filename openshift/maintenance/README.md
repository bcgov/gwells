# Groundwater Wells

## Maintenance Mode

### Usage

Caddy pods serving static html are deployed to our prod, dev and test environments.  To enable maintenance mode switch the routes between the GWells and Proxy-Caddy services.  A namespace (project) for deployment must be specified.

Expected namespaces:

* moe-gwells-prod
* moe-gwells-dev
* moe-gwells-test

For the sake of simplicity all examples will use moe-gwells-test and be run on OS X.

1. ##### Enable/Disable by Script

    Maintenance mode on.

    ```
    ./maintenance.sh moe-gwells-test on
    ```

    Maintenance mode off.

    ```
    ./maintenance.sh moe-gwells-test off
    ```

2. ##### Enable/Disable by Command line

    Maintenance mode on.

    ```
    oc patch route gwells -n moe-gwells-test -p \
        '{ "spec": { "to": { "name": "proxy-caddy", "port": { "targetPort": "2015-tcp" }}}'
    oc patch route proxy-caddy -n moe-gwells-test -p \
        '{ "spec": { "to": { "name": "gwells" }, "port": { "targetPort": "web" }}}'
    ```

    Maintenance mode off.

    ```
    oc patch route gwells -n moe-gwells-test -p \
        '{ "spec": { "to": { "name": "gwells" }, "port": { "targetPort": "web" }}}'
    oc patch route proxy-caddy -n moe-gwells-test -p \
        '{ "spec": { "to": { "name": "proxy-caddy" }, "port": { "targetPort": "2015-tcp" }}}'
    ```

### Build and Deployment

This application's template has been broken down into build and deploy components.

##### Build

Template:

* ../openshift/templates/caddy.bc.json

Contains:

* ImageStream
* BuildConfig

Default vars:

* NAME: proxy-caddy
* IMG_SRC: bcgov-s2i-caddy
* GIT_REPO: https://github.com/bcgov/gwells.git
* GIT_BRANCH: master

Build Project:

* moe-gwells-tools


1. ##### Build by Script

    ```
    ./maintenance.sh moe-gwells-tools build
    ```

2. ##### Build by Command line

    ```
    oc process -f ../openshift/templates/caddy.bc.json -p NAME=proxy-caddy \
      GIT_REPO=https://github.com/bcgov/gwells.git GIT_BRANCH=master \
      IMG_SRC=bcgov-s2i-caddy | oc apply -f -

    ```

##### Deploy

Template:

* ../openshift/templates/caddy.dc.json

Contains:

* DeploymentConfig
* Service

Default vars:

* NAME: proxy-caddy
* BUILD_PROJECT: moe-gwells-tools

Build (Source) Project:

* moe-gwells-tools

Deploy Projects Available:

* moe-gwells-test
* moe-gwells-dev
* moe-gwells-prod


1. ##### Deploy by Script

    ```
    ./maintenance.sh moe-gwells-tools deploy
    ```

2. ##### Deploy by Command line

    ```
    oc process -f ../openshift/templates/caddy.bc.json -n moe-gwells-tools -p NAME=proxy-caddy \
        BUILD_PROJECT=moe-gwells-tools | oc apply -f -
    oc expose svc proxy-caddy
    ```

### Initial Setup

Starting from scratch the above steps will be reordered:

1. Build
2. Deploy
3. Maintenance on
4. Maintenance off

## License

Code released under the [Apache License, Version 2.0](https://github.com/bcgov/gwells/blob/master/LICENSE).
