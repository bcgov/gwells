#!/bin/sh
#
# Run all api (newman/postman) tests locally.

set -e

./local_aquifers.sh
./local_registries.sh
./local_submissions.sh
./local_wells_search.sh
./local_wells.sh
