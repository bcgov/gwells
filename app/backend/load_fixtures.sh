#!/bin/bash


# Halt on errors/unsets, change fail returns, change field separator, verbose mode
#
set -euo pipefail
IFS=$'\n\t'
[ "${VERBOSE:-}" == true ]&& set -x


# Parameters and defaults
#
COMMAND=${1:-"all"}
FIXTURE_SET=(
	"gwells-codetables.json"
	"wellsearch-codetables.json"
	"registries-codetables.json"
	"registries.json"
	"wellsearch.json"
	"aquifers.json"
)


# Show message if pano params
#
if [ "${#}" -lt 1 ]
then
	echo
	echo "Load Fixtures"
	echo
	echo "Specify which fixtures to load or 'all' for everything."
	echo " './load_fixtures.sh <all|fixture.json>'"
	echo
	echo "Set variables to non-defaults at runtime.  E.g.:"
	echo " 'VERBOSE=true FIXTURE_SET="fix1.json fix2.json" ./load_fixtures.sh all'"
	echo
	exit
fi


# Action based on parameter
#
if [ "${COMMAND}" == "all" ]
then
	for f in ${FIXTURE_SET[@]}
	do
		python manage.py loaddata $f
	done
else
	python manage.py loaddata "${COMMAND}"
fi
