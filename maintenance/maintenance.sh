#!/bin/bash


# Halt on errors/unsets, change fail returns, change field separator
#
set -euo pipefail
IFS=$'\n\t'


# Parameters and mode variables
#
PROJECT=${1:-}
COMMAND=${2:-}
VERBOSE=${VERBOSE:-}


# App and build settings
#
APPLICATION=${APPLICATION:-gwells}
APPLICATION_PORT=${APPLICATION_PORT:-web}
STATIC_PAGE=${STATIC_PAGE:-proxy-caddy}
STATIC_PAGE_PORT=${STATIC_PAGE_PORT:-2015-tcp}
#
IMG_NAME=${IMG_NAME:-bcgov-s2i-caddy}
GIT_REPO=${GIT_REPO:-https://github.com/bcgov/gwells.git}
GIT_BRANCH=${GIT_BRANCH:-master}
OC_BUILD=${OC_BUILD:-../openshift/templates/caddy-build.json}
OC_DEPLOY=${OC_DEPLOY:-../openshift/templates/caddy-deploy.json}


# Verbose option
#
[ "${VERBOSE}" == true ]&& \
	set -x


# Show message if passed any params
#
if [ "${#}" -lt 2 ]
then
	echo
	echo "Maintenace Mode: Caddy served static page"
	echo
	echo "Provide a project and a command."
	echo " './maintenance.sh <project_name> <maint-on|maint-off|build|deploy>'"
	echo
	echo "Set variables to non-defaults at runtime.  E.g.:"
	echo " 'VERBOSE=true GIT_BRANCH=master ./maintenance.sh <...>'"
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


# Action based on parameter
#
if [ "${COMMAND}" == "maint-on" ]
then
	oc patch route ${APPLICATION} -n ${PROJECT} -p \
		'{ "spec": { "to": { "name": "'$( echo ${STATIC_PAGE} )'" },
		"port": { "targetPort": "'$( echo ${STATIC_PAGE_PORT} )'" }}}'
	oc patch route ${STATIC_PAGE} -n ${PROJECT} -p \
		'{ "spec": { "to": { "name": "'$( echo ${APPLICATION} )'" },
		"port": { "targetPort": "'$( echo ${APPLICATION_PORT} )'" }}}'
elif [ "${COMMAND}" == "maint-off" ]
then
	oc patch route ${APPLICATION} -n ${PROJECT} -p \
		'{ "spec": { "to": { "name": "'$( echo ${APPLICATION} )'" },
		"port": { "targetPort": "'$( echo ${APPLICATION_PORT} )'" }}}'
	oc patch route ${STATIC_PAGE} -n ${PROJECT} -p \
		'{ "spec": { "to": { "name": "'$( echo ${STATIC_PAGE} )'" },
		"port": { "targetPort": "'$( echo ${STATIC_PAGE_PORT} )'" }}}'
elif [ "${COMMAND}" == "build" ]
then
	oc process -f ${OC_BUILD} \
		-p NAME=${STATIC_PAGE} GIT_REPO=${GIT_REPO} GIT_BRANCH=${GIT_BRANCH} IMG_NAME=${IMG_NAME} \
		| oc apply -f -
elif [ "${COMMAND}" == "deploy" ]
then
	oc process -f ${OC_DEPLOY} -n ${PROJECT} -p NAME=${STATIC_PAGE} BUILD_PROJECT=${PROJECT} \
		| oc apply -f -
	oc get route ${STATIC_PAGE} || \
		oc expose svc ${STATIC_PAGE}
	oc get dc ${STATIC_PAGE} -o json | grep '"image":' | awk '{ print $2 }' | tr -d ',"' \
		| tee -a ./container_img.log
else
	echo
	echo "Parameter '${COMMAND}' not understood."
	echo
fi
