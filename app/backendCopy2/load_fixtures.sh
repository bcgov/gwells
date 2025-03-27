#!/bin/bash


# Halt on errors/unsets, change fail returns, change field separator, verbose mode
#
set -euo pipefail
IFS=$'\n\t'
[ "${VERBOSE:-}" == true ]&& set -x


# Parameters and defaults
#
COMMAND=${1:-"all"}
FIXTURES=(
	"gwells-codetables.json"
	"wellsearch-codetables.json"
	"registries-codetables.json"
	"registries.json"
	"wellsearch.json"
	"aquifers.json"
)


# Show message if pano params
#
if [ "${#}" -eq 0 ]
then
	echo
	echo "Load Fixtures"
	echo
	echo "Specify which fixtures to load or 'all' for everything."
	echo " './load_fixtures.sh <all|fixture.json>'"
	echo
	exit
fi


# Action based on parameter
#
if [ "${COMMAND}" == "all" ]
then
	for f in ${FIXTURES[@]}
	do
		echo python manage.py loaddata $f
		python manage.py loaddata $f
	done
else
	python manage.py loaddata "${COMMAND}"
fi
