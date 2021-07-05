#!/bin/bash
# Usage: ./reset_migration.sh [test/prod]

echo "WARNING! This will not reset the database. This script will only reverse the proxy and pod scaling."
. ./activate_proxy "$1" --revert
. ./scale_up.sh "$1" --revert
. ./scale_down.sh "$1" --revert
