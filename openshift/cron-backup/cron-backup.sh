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
SCRIPT_DIR=$(dirname $0)
OC_BUILD=${OC_BUILD:-${SCRIPT_DIR}/../backup.bc.yaml}
OC_DEPLOY=${OC_DEPLOY:-${SCRIPT_DIR}/../backup.cj.yaml}
#
DRY_RUN=${DRY_RUN:-false}
SCHEDULE=${SCHEDULE:-}


# Show message if passed any params
#
if [ "${#}" -ne 1 ]
then
	set +x
	echo
	echo "PostgreSQL Backup Cronjobs"
	echo
	echo "Setup backup cronjobs for a PostgreSQL deployment."
	echo "Defaults to 11 AM UTC (3 AM PDT, 0 11 * * *)."
	echo "Override defaults with runtime variables."
	echo
	echo "Usage:"
	echo "  ./cron-backup.sh [project]/[database]"
	echo
	echo "Examples:"
	echo "  # Deploy to staging environment"
	echo "  ./cron-backup.sh moe-gwells-test/gwells-pgsql-staging"
	echo
	echo "  # Deploy to demo environment, custom testing schedule"
	echo "  SCHEDULE=\"*/5 * * * *\" ./cron-backup.sh moe-gwells-test/gwells-pgsql-demo"
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