#!/bin/bash
# ---------------------------------------------------------------------------------
# Require all needed input/params for migration
# ---------------------------------------------------------------------------------
# running source on params.sh takes care of all needed parameters
# First thing it does is ask what environment we're doing the migration for
. ./params.sh

# Require login upfront
. ./require_pathfinder_auth.sh
. ./require_silver_auth.sh

# scale down

# ---------------------------------------------------------------------------------
# Migrate the database
# ---------------------------------------------------------------------------------
. ./migrate_database.sh

# ---------------------------------------------------------------------------------
# Mirror minio data
# ---------------------------------------------------------------------------------
. ./migrate_minio.sh