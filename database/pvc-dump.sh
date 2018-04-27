#!/bin/sh
#
# Dumps from a GWells database and stores locally.  Project namespace required.
#
#
# NOTE: You need to be logged in with a token, via:
#       https://console.pathfinder.gov.bc.ca:8443/oauth/token/request


# Halt conditions, verbosity and field separator
#
set -euo pipefail
[ "${VERBOSE:-x}" != true ]|| set -x
IFS=$'\n\t'


# Parameters
#
PROJECT=${1:-}
SAVE_TO=${2:-/var/lib/pgsql/backup/$( date +%Y-%m-%d-%T ).gz}


# APP and mode variables
#
APP_NAME=${APP_NAME:-gwells}
DB_NAME=${DB_NAME:-${APP_NAME}}
KEEP_APP_ONLINE=${KEEP_APP_ONLINE:-false}


# Repo directory
#
REPO_DIR=$( git rev-parse --show-toplevel )


# Put GWells into maintenance mode and scale down (deployment config)
#
if [ "${KEEP_APP_ONLINE}" != "true" ]
then
	APPLICATION_NAME=${APP_NAME} ${REPO_DIR}/maintenance/maintenance.sh ${PROJECT} on
	oc scale -n ${PROJECT} --replicas=0 deploymentconfig ${APP_NAME}
fi


# Identify database and take a backup
#
POD_DB=$( oc get pods -n ${PROJECT} -o name | grep -Eo "postgresql-[0-9]+-[[:alnum:]]+" )
oc exec ${POD_DB} -n ${PROJECT} -- /bin/bash -c 'pg_dump '${DB_NAME}' | gzip > '${SAVE_TO}


# Take GWells out of maintenance mode and scale back up (deployment config)
#
if [ "${KEEP_APP_ONLINE}" != "true" ]
then
	oc scale -n ${PROJECT} --replicas=1 deploymentconfig ${APP_NAME}
	sleep 30
	APPLICATION_NAME=${APP_NAME} ${REPO_DIR}/maintenance/maintenance.sh ${PROJECT} off
fi
