#!/bin/sh
#
# Fri Mar 23 11:12:37 2018 GW Shell script to copy over sanizited legacy MS Access
# tables via 'oc rsync' on the postgres Pod.  This script runs on a local developer
# workstation, calling remote 'oc exec' commands
#
# NOTE: You need to be logged in with a token, via:
#       https://console.pathfinder.gov.bc.ca:8443/oauth/token/request
#
# Running on postgres database pod, as DB root access not enabled on gwells application pod
# DEV


# Halt conditions, verbosity and field separator
#
set -euo pipefail
[ "${VERBOSE:-x}" != true ]|| set -x
IFS=$'\n\t'


# Parameters and mode variables
#
PROJECT=${1:-}


# Show message if passed any params
#
if [ "${#}" -eq 0 ]
then
	echo
	echo "Provide a project name."
	echo " './setup-xfer.sh <project_name>'"
	echo
	exit
fi


# Check login
#
if( ! oc whoami )
then
    echo
    echo "Please obtain an OpenShift API token.  A window will open shortly."
    sleep 3
    open https://console.pathfinder.gov.bc.ca:8443/oauth/token/request
    exit
fi


# Check project
#
CHECK=$( oc projects | tr -d '*' | grep -v "Using project" | grep "${PROJECT}" | awk '{ print $1 }' || echo )
if [ "${PROJECT}" != "${CHECK}" ]
then
	echo
	echo "Unable to access project ${PROJECT}"
	echo
	exit
fi


oc project moe-gwells-dev
podname=$(oc get pods -n moe-gwells-dev | grep gwells-[0-9] | grep Running | head -n 1 | awk '{print $1}')
oc rsync /Users/garywong/projects/registry-gwells-export/2018-APR-16.sanitized  $podname:/tmp
oc exec ${podname} -n moe-gwells-dev -- /bin/bash -c 'cp --remove-destination /tmp/2018-APR-16.sanitized/*.sanitized.csv  /opt/app-root/src/database/code-tables/registries/'
oc exec ${podname} -n moe-gwells-dev -- /bin/bash -c 'export PGPASSWORD=$DATABASE_PASSWORD;cd /opt/app-root/src/database/code-tables/registries/;psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  << EOF
\ir ../../scripts/registries/post-deploy.sql
\i clear-tables.sql
\ir ../../scripts/registries/initialize-xforms-registries.sql
\i data-load-static-codes.sql
\ir ../../scripts/registries/populate-registries-from-xform.sql
EOF
'
# TEST
oc project moe-gwells-test
podname=$(oc get pods -n moe-gwells-test | grep gwells-[0-9] | grep Running | head -n 1 | awk '{print $1}')
oc rsync /Users/garywong/projects/registry-gwells-export/2018-APR-16.sanitized  $podname:/tmp
oc exec ${podname} -n moe-gwells-test -- /bin/bash -c 'cp --remove-destination /tmp/2018-APR-16.sanitized/*.sanitized.csv  /opt/app-root/src/database/code-tables/registries/'
oc exec ${podname} -n moe-gwells-test -- /bin/bash -c 'export PGPASSWORD=$DATABASE_PASSWORD;cd /opt/app-root/src/database/code-tables/registries/;psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  << EOF
\ir ../../scripts/registries/post-deploy.sql
\i clear-tables.sql
\ir ../../scripts/registries/initialize-xforms-registries.sql
\i data-load-static-codes.sql
\ir ../../scripts/registries/populate-registries-from-xform.sql
EOF
'
