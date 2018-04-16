${PROJECT}#!/bin/bash


# Halt on errors/unsets, change fail returns, change field separator
#
set -euo pipefail
IFS=$'\n\t'


# Parameters and mode variables
#
PROJECT=${1:-}
COMMAND=${2:-}
VERBOSE=${VERBOSE:-false}


# App settings
#
APP_MAINT_OFF=${APP_MAINT_OFF:-gwells}
APP_MAINT_ON=${APP_MAINT_ON:-proxy-caddy}
PORT_MAINT_OFF=${PORT_MAINT_OFF:-web}
PORT_MAINT_ON=${PORT_MAINT_ON:-2015-tcp}


# Server and build settings
#
IMG_NAME=${IMG_NAME:-bcgov-s2i-caddy}
GIT_REPO=${GIT_REPO:-https://github.com/bcgov/gwells.git}
GIT_BRANCH=${GIT_BRANCH:-master}
OC_SERVER=${OC_SERVER:-https://console.pathfinder.gov.bc.ca:8443}
OC_TEMPLATE_BUILD=${OC_TEMPLATE_BUILD:-../openshift/templates/caddy-build.json}
OC_TEMPLATE_DEPLOY=${OC_TEMPLATE_DEPLOY:-../openshift/templates/caddy-deploy.json}


# Verbose option
#
[ "${VERBOSE}" == true ]&& \
	set -x


# Check project
#
PROJECT_CHECK=$( oc projects | tr -d '*' | grep -v "Using project" | grep "${PROJECT}" | awk '{ print $1 }' || echo )
if [ "${PROJECT}" != "${PROJECT_CHECK}" ]
then
	echo
	echo "Unable to access project ${PROJECT}"
	echo
	exit
fi


# Show message if passed any params
#
if [ "${#}" -lt 2 ]||[ "${PROJECT}" == "help" ]
then
	echo
	echo "Deploy Caddy to allow maintenance or downtime messages."
	echo
	echo "Provide at least one parameter."
	echo " './maintenance.sh maintenance-on|maintenance-off|build|deploy'"
	echo
	echo "Set variables to non-defaults at runtime.  E.g.:"
	echo " 'VERBOSE=true ./maintenance.sh <...>'"
	echo
	exit
fi


# Action based on parameter
#
if [ "${COMMAND}" == "maint-on" ]
then
	oc patch route ${APP_MAINT_OFF} -n ${PROJECT} -p \
		'{ "spec": { "to": { "name": "'$( echo ${APP_MAINT_ON} )'" }, "port": { "targetPort": "'$( echo ${PORT_MAINT_ON} )'" }}}'
	oc patch route ${APP_MAINT_ON} -n ${PROJECT} -p \
		'{ "spec": { "to": { "name": "'$( echo ${APP_MAINT_OFF} )'" }, "port": { "targetPort": "'$( echo ${PORT_MAINT_OFF} )'" }}}'
elif [ "${COMMAND}" == "maint-off" ]
then
	oc patch route ${APP_MAINT_OFF} -n ${PROJECT} -p \
		'{ "spec": { "to": { "name": "'$( echo ${APP_MAINT_OFF} )'" }, "port": { "targetPort": "'$( echo ${PORT_MAINT_OFF} )'" }}}'
	oc patch route ${APP_MAINT_ON} -n ${PROJECT} -p \
		'{ "spec": { "to": { "name": "'$( echo ${APP_MAINT_ON} )'" }, "port": { "targetPort": "'$( echo ${PORT_MAINT_ON} )'" }}}'
elif [ "${COMMAND}" == "build" ]
then
	oc process -f ${OC_TEMPLATE_BUILD} -p NAME=${APP_MAINT_ON} GIT_REPO=${GIT_REPO} GIT_BRANCH=${GIT_BRANCH} IMG_NAME=${IMG_NAME} | oc apply -f -
elif [ "${COMMAND}" == "deploy" ]
then
	oc process -f ${OC_TEMPLATE_DEPLOY} -n ${PROJECT} \
		-p NAME=${APP_MAINT_ON} BUILD_PROJECT=${PROJECT} \
		| oc apply -f -
	[ "${APP_MAINT_OFF}" == "${APP_MAINT_ON}" ] && oc get route ${APP_MAINT_ON} || \
		oc expose svc ${APP_MAINT_ON}
	oc get dc ${APP_MAINT_ON} -o json | grep '"image":' | awk '{ print $2 }' | tr -d ',"' >> ./container_img.log
elif [ "${COMMAND}" == "nuke" ]
then
	oc delete all -l app=${APP_MAINT_ON}
else
	echo
	echo "Parameter '${COMMAND}' not understood."
	echo
fi
