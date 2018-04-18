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
if ( ! oc whoami )
then
    echo
    echo "Please obtain an OpenShift API token.  A window will open shortly."
    sleep 3
    open https://console.pathfinder.gov.bc.ca:8443/oauth/token/request
    exit
fi


# Check project availability
#
CHECK=$( oc projects | tr -d '*' | grep -v "Using project" | grep "${PROJECT}" | awk '{ print $1 }' || echo )
if [ "${PROJECT}" != "${CHECK}" ]
then
	echo
	echo "Unable to access project ${PROJECT}"
	echo
	exit
fi


# Identify running GWells pod under selected project
#
PODNAME=$( oc get pods -n ${PROJECT} | grep gwells-[0-9] | grep Running | head -n 1 | awk '{print $1}' )


# Use oc rsync to copy into the pod and move to the correct dir
#
oc rsync /Users/garywong/projects/registry-gwells-export/2018-APR-16.sanitized  $PODNAME:/tmp
oc exec ${PODNAME} -n ${PROJECT} -- /bin/bash -c 'cp --remove-destination /tmp/2018-APR-16.sanitized/*.sanitized.csv  /opt/app-root/src/database/code-tables/registries/'


# Run post-deploy and other scripts
#
SCRIPTS=(
    "/opt/app-root/src/database/scripts/registries/post-deploy.sql"
    "/opt/app-root/src/database/code-tables/registries/clear-tables.sql"
    "/opt/app-root/src/database/scripts/registries/initialize-xforms-registries.sql"
    "/opt/app-root/src/database/code-tables/registries/data-load-static-codes.sql"
    "/opt/app-root/src/database/scripts/registries/populate-registries-from-xform.sql"
)
for s in ${SCRIPTS[@]}
do
    DIR=$( dirname $s )
    SQL=$( basename $s )
    echo
    echo " >> $s"
    oc exec ${PODNAME} -n ${PROJECT} -- /bin/bash -c 'export PGPASSWORD=$DATABASE_PASSWORD; cd '${DIR}'; psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f ./'${SQL}
done
