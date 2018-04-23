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
SAVE_TO=${2:-./$(date +%Y-%m-%d-%T)}


# APP and mode variables
#
APPLICATION_NAME=${APPLICATION_NAME:-gwells}
APPLICATION_PORT=${APPLICATION_PORT:-web}
DB_NAME=${DB_NAME:-gwells}
KEEP_APP_ONLINE=${KEEP_APP_ONLINE:-true}


# Show message if passed any params
#
if [ "${#}" -eq 0 ]||[ "${#}" -gt 2 ]
then
	echo
    echo "Dumps from a GWells database to store locally"
    echo
	echo "Provide a project name."
	echo " './oc-dump.sh <project_name> <optional:output_file>'"
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
REPO_DIR=$( git rev-parse --show-toplevel )
if [ "${KEEP_APP_ONLINE}" != "true" ]
then
	cd ${REPO_DIR}/maintenance/;
	APPLICATION_NAME=${APPLICATION_NAME} APPLICATION_PORT=${APPLICATION_PORT} ./maintenance.sh ${PROJECT} on;
	oc scale -n ${PROJECT} --replicas=0 deploymentconfig ${APPLICATION_NAME}
fi


# Identify database and take a backup
#
POD_DB=$( oc get pods -n ${PROJECT} -o name | grep -Eo "postgresql-[0-9]+-[[:alnum:]]+" )
