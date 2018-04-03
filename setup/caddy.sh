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
APP_NAME=${APP_NAME:-proxy-caddy}
GIT_REPO=${GIT_REPO:-https://github.com/gwells/gwells.git}
GIT_BRANCH=${GIT_BRANCH:-master}
OC_SERVER=${OC_SERVER:-https://console.pathfinder.gov.bc.ca:8443}
OC_TEMPLATE_BUILD=${OC_TEMPLATE_BUILD:-../openshift/templates/caddy-build.json}
OC_TEMPLATE_DEPLOY=${OC_TEMPLATE_DEPLOY:-../openshift/templates/caddy-deploy.json}


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
	oc patch route ${APP_NAME} -p '{ "spec": { "to": { "name": "proxy-caddy" }, "port": { "targetPort": "2015-tcp" }}}'
elif [ "${PARAM}" == "maint-off" ]
then
	oc patch route ${APP_NAME} -p '{ "spec": { "to": { "name": "jenkins" }, "port": { "targetPort": "web" }}}'
elif [ "${PARAM}" == "build" ]
then
	oc process -f ${OC_TEMPLATE_BUILD} -p NAME=${APP_NAME} GIT_REPO=${GIT_REPO} GIT_BRANCH=${GIT_BRANCH} IMG_NAME=${IMG_NAME} | oc apply -f -
elif [ "${PARAM}" == "deploy" ]
then
	oc process -f ${OC_TEMPLATE_DEPLOY} -p NAME=${APP_NAME} | oc apply -f -
	oc expose svc ${APP_NAME}
else
	echo
	echo "Parameter '${PARAM}' not understood."
	echo
fi
