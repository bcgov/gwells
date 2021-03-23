#!/bin/bash
# Usage ./do_migration.sh |& tee /tmp/migration.log

# ---------------------------------------------------------------------------------
# Require all needed input/params for migration
# ---------------------------------------------------------------------------------
# running source on params.sh takes care of all needed parameters
# First thing it does is ask what environment we're doing the migration for
. ./params.sh

# Require login upfront
. ./require_pathfinder_auth.sh
. ./require_silver_auth.sh

# Scale down the gwells application on Pathfinder and Silver
. ./scale_down.sh

# Migrate the database
. ./migrate_database.sh

# Mirror minio data
. ./migrate_minio.sh

if [ "$TEST_RUN" == 0 ]; then
  # Scale up the gwells application on Silver
  . ./scale_up.sh

  # Activate the proxy
  . ./activate_proxy.sh
fi