#!/bin/bash


# Halt on errors/unsets, change fail returns, change field separator, verbose mode
#
set -euo pipefail
IFS=$'\n\t'
[ "${VERBOSE:-}" != true ]|| set -x


# Parameters and mode variables
#
PARAM=${1:-""}
PROJECT=$( echo ${PARAM} | cut -d "/" -f 1 )
TARGET=$( echo ${PARAM} | cut -d "/" -f 2 )

# App and build settings
#
OC_BUILD=${OC_BUILD:-../backup.bc.yaml}
OC_DEPLOY=${OC_DEPLOY:-../backup.cj.yaml}
#
DRY_RUN=${DRY_RUN:-false}
SCHEDULE=${SCHEDULE:-}


# Show message if passed any params
#
if [ "${#}" -ne 1 ]
then
	set +x
	echo
	echo "PostgreSQL Backup Cronjob:"
	echo
	echo "Provide a project and a command."
	echo " ./cron-backup.sh PROJECT/TARGET"
	echo
	echo "Set variables to non-defaults at runtime.  E.g.:"
	echo " VERBOSE=true SCHEDULE=\"*/5 * * * *\" ./cron-backup.sh <...>"
	echo
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


# Create build config and image
#
oc process -f ${OC_BUILD} \
	| oc apply -n moe-gwells-tools -f -


# Deploy, add SCHEDULE is provided
#
if [ -z "${SCHEDULE}" ]
then
	oc process -f ${OC_DEPLOY} -p TARGET=${TARGET} \
		| oc apply -n ${PROJECT} -f -
else
	oc process -f ${OC_DEPLOY} -p TARGET=${TARGET} -p SCHEDULE=${SCHEDULE} \
		| oc apply -n ${PROJECT} -f -
fi