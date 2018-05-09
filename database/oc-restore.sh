#!/bin/sh
#
# Dumps from a GWells database and stores locally.  Project namespace required.
#
# Based on TFRS' process:
#	https://github.com/bcgov/gwells/tree/developer/database/xfer-registries-to-openshift
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
RESTORE=${2:-./${PROJECT}-$(date +%Y-%m-%d-%T)}


# APP and mode variables
#
APP_NAME=${APP_NAME:-gwells}
DB_NAME=${DB_NAME:-${APP_NAME}}
KEEP_APP_ONLINE=${KEEP_APP_ONLINE:-false}


# Show message if passed any params
#
if [ "${#}" -ne 2 ]
then
	echo
    echo "Restores a GWells database from a local file"
    echo
	echo "Provide a project name."
	echo " './oc-restore.sh <project_name> <input_file>'"
	echo
	exit
fi


# Check login
#
if ! oc whoami
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


# Put GWells into maintenance mode and scale down (deployment config)
#
if [ "${KEEP_APP_ONLINE}" != "true" ]
then
	APPLICATION_NAME=${APP_NAME} ../maintenance/maintenance.sh ${PROJECT} on
	oc scale -n ${PROJECT} --replicas=0 deploymentconfig ${APP_NAME}
fi


# Identify database and take a backup
#
POD_DB=$( oc get pods -n ${PROJECT} -o name | grep -Eo "postgresql-[0-9]+-[[:alnum:]]+" )


# Take GWells out of maintenance mode and scale back up (deployment config)
#
if [ "${KEEP_APP_ONLINE}" != "true" ]
then
	oc scale -n ${PROJECT} --replicas=1 deploymentconfig ${APP_NAME}
	sleep 30
	APPLICATION_NAME=${APP_NAME} ../maintenance/maintenance.sh ${PROJECT} off
fi


# Summarize
#
echo
echo "DB:   ${DB_NAME}"
echo "Size: $( du -h ${RESTORE} | awk '{ print $1 }' )"
echo "Name: ${RESTORE}"
echo
