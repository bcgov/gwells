#!/bin/sh
#
# Dumps from a GWells database and stores locally.  Project namespace required.
#
# NOTE: You need to be logged in with a token, via:
#       https://console.pathfinder.gov.bc.ca:8443/oauth/token/request


# Halt conditions, verbosity and field separator
#
set -euo pipefail
[ "${VERBOSE:-x}" != true ]|| set -x
IFS=$'\n\t'


# Params and env vars
#
SAVE_TO=${1:-/var/lib/pgsql/backup/$( date +%Y-%m-%d-%T ).gz}
BK_COUNT=${BK_COUNT:-10}
DB_NAME=${DB_NAME:-gwells}


# Identify database and take a backup
#
mkdir -p $( dirname ${SAVE_TO} )
pg_dump ${DB_NAME} | gzip > ${SAVE_TO}


# Cleanup any more than BK_COUNT backups
#
ls /var/lib/pgsql/backup/*.gz -1pr | tail -n +$( expr 1 + ${BK_COUNT} )| xargs -r rm --


# Summarize
#
echo
echo "DB:   ${DB_NAME}"
echo "Size: $( du -h ${SAVE_TO} | awk '{ print $1 }' )"
echo "Name: ${SAVE_TO}"
echo
