#!/bin/sh
#
# Run all api (newman/postman) tests locally.
source ./.envrc
set -e

./local_aquifers.sh
./local_registries.sh
./local_submissions.sh
./local_wells_search.sh
./local_wells.sh

echo "Environment variables (including your password) will not persist after this terminal is closed"
