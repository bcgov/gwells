#!/bin/bash


# Halt on errors/unsets, change fail returns, change field separator
#
set -euo pipefail
IFS=$'\n\t'


# Parameters and mode variables
#
PARAM=${1:-}
VERBOSE=${VERBOSE:-false}


# Server and build settings
#
IMG_NAME=${IMG_NAME:-bcgov-s2i-caddy}
GIT_REPO=${GIT_REPO:-https://github.com/bcgov/gwells.git}
GIT_BRANCH=${GIT_BRANCH:-master}
BUILD_PROJECT=${BUILD_PROJECT:-moe-gwells-tools}
OC_SERVER=${OC_SERVER:-https://console.pathfinder.gov.bc.ca:8443}
OC_TEMPLATE_BUILD=${OC_TEMPLATE_BUILD:-../openshift/templates/caddy-build.json}
OC_TEMPLATE_DEPLOY=${OC_TEMPLATE_DEPLOY:-../openshift/templates/caddy-deploy.json}


# App settings
#
APP_MAINT_OFF=${APP_MAINT_OFF:-gwells}
APP_MAINT_ON=${APP_MAINT_ON:-proxy-caddy}
APP_REDIRECT=${APP_REDIRECT:-$APP_MAINT_ON}


# Verbose option
#
[ "${VERBOSE}" == true ]&& \
	set -x


# Show message if passed any params
#
if [ "${#}" -eq 0 ]
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
if [ "${PARAM}" == "maint-on" ]
then
	JSON='{ "spec": { "to": { "name": "'$( echo ${APP_MAINT_ON} )'" }, "port": { "targetPort": "2015-tcp" }}}'
	oc patch route ${APP_REDIRECT} -p ${JSON}
elif [ "${PARAM}" == "maint-off" ]
then
	JSON='{ "spec": { "to": { "name": "'$( echo ${APP_MAINT_OFF} )'" }, "port": { "targetPort": "web" }}}'
	oc patch route ${APP_REDIRECT} -p ${JSON}
elif [ "${PARAM}" == "build" ]
then
	oc process -f ${OC_TEMPLATE_BUILD} -p NAME=${APP_MAINT_ON} GIT_REPO=${GIT_REPO} GIT_BRANCH=${GIT_BRANCH} IMG_NAME=${IMG_NAME} | oc apply -f -
elif [ "${PARAM}" == "deploy" ]
then
	oc process -f ${OC_TEMPLATE_DEPLOY} -p NAME=${APP_MAINT_ON} BUILD_PROJECT=${BUILD_PROJECT} | oc apply -f -
	[ "${APP_REDIRECT}" == "${APP_MAINT_ON}" ] && oc get route ${APP_MAINT_ON} || oc expose svc ${APP_MAINT_ON}
	CONTAINER_IMG=$( oc get dc proxy-caddy -o json | grep '"image":' | awk '{ print $2 }' | tr -d ',"' )
	echo "${CONTAINER_IMG}" >> ./container_img.log
elif [ "${PARAM}" == "nuke" ]
then
	oc delete all -l app=${APP_MAINT_ON}
else
	echo
	echo "Parameter '${PARAM}' not understood."
	echo
fi
