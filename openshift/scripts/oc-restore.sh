#!/bin/sh
#
# Dumps from a GWells database and stores locally.  Project namespace required.
#
# Based on TFRS' process:
#	https://github.com/bcgov/gwells/tree/developer/database/xfer-registries-to-openshift
#
# NOTE: You need to be logged in with a token, via:
#       https://console.pathfinder.gov.bc.ca:8443/oauth/token/request
#
# EXAMPLE: ./oc-restore.sh moe-gwells-prod/gwells-pgsql-production gwells-pgsql-production-2018-12-20-1542.dump 


# Halt conditions, verbosity and field separator
#
set -euo pipefail
[ "${VERBOSE:-x}" != true ]|| set -x
IFS=$'\n\t'


# Parameters
#
TARGET=${1:-}
RESTORE=${2:-}
PROJECT=$( echo ${TARGET} | cut -d "/" -f 1 )
DC_NAME=$( echo ${TARGET} | cut -d "/" -f 2 )


# APP and mode variables
#
APP_NAME=${APP_NAME:-gwells}
DB_NAME=${DB_NAME:-${APP_NAME}}
KEEP_APP_ONLINE=${KEEP_APP_ONLINE:-true}


# Show message if passed any params
#
if [ "${#}" -ne 2 ]
then
	echo
    echo "Restores a GWells database from a local file"
    echo
	echo "Provide a target name and backup file to restore."
	echo " './oc-restore.sh <project_name>/<deploymentconfig_name> <input_file>'"
	echo
	exit
fi


# Verify ${RESTORE} file
#
if [ ! -f "${RESTORE}" ]
then
	echo
	echo "Please verify ${RESTORE} exists and is non-empty.  Exiting."
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


# Copy dump into pod
#
RESTORE_PATH=$( dirname ${RESTORE} )
RESTORE_FILE=$( basename ${RESTORE} )
POD_DB=$( oc get pods -n ${PROJECT} -o name | grep -Eo "${DC_NAME}-[[:digit:]]+-[[:alnum:]]+" )
oc cp ${RESTORE} "${POD_DB}":/tmp/ -n ${PROJECT}


# Drop tables and functions from ./db-drops.sql
#
while read c
do
	oc exec ${POD_DB} -n ${PROJECT} -- /bin/bash -c "psql -d ${DB_NAME} -U \${POSTGRESQL_USER} -c \"${c}\""
done < db-drops.sql


# Restore database dump
#
oc exec ${POD_DB} -n ${PROJECT} -- /bin/bash -c "pg_restore -d ${DB_NAME} -U \${POSTGRESQL_USER} --no-owner /tmp/${RESTORE_FILE}"


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
echo "Name: ${DC_NAME}"
echo "Proj: ${PROJECT}"
echo "DB:   ${DB_NAME}"
echo "Size: $( du -h ${RESTORE} | awk '{ print $1 }' )"
echo "File: ${RESTORE}"
echo
