#!/bin/sh
#
# Fri Mar 23 11:12:37 2018 GW Shell script to copy over sanizited legacy MS Access 
# tables via 'oc rsync' on the postgres Pod.  This script runs on a local developer
# workstation, calling renote 'oc exec' commands
#
# NOTE: You need to be logged in with a token, via:
#       https://console.pathfinder.gov.bc.ca:8443/oauth/token/request
#
# Running on postgres database pod, as DB root access not enabled on gwells application pod
# DEV
oc project moe-gwells-dev
podname=$(oc get pods -n moe-gwells-dev | grep gwells-[0-9] | grep Running | head -n 1 | awk '{print $1}')
oc rsync /Users/garywong/projects/registry-gwells-export/2018-MAR-28.sanitized  $podname:/tmp
oc exec ${podname} -n moe-gwells-dev -- /bin/bash -c 'cp --remove-destination /tmp/2018-MAR-28.sanitized/*.sanitized.csv  /opt/app-root/src/database/code-tables/registries/'
oc exec ${podname} -n moe-gwells-dev -- /bin/bash -c 'export PGPASSWORD=$DATABASE_PASSWORD;cd /opt/app-root/src/database/code-tables/registries/;psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  << EOF
\i clear-tables.sql
\ir ../../scripts/registries/populate-xforms-registries.sql
\i data-load-static-codes.sql
\ir ../../scripts/registries/populate-registries-from-xform.sql
\ir ../../scripts/registries/post-deploy.sql
EOF
'
# TEST
oc project moe-gwells-test
podname=$(oc get pods -n moe-gwells-test | grep gwells-[0-9] | grep Running | head -n 1 | awk '{print $1}')
oc rsync /Users/garywong/projects/registry-gwells-export/2018-MAR-28.sanitized  $podname:/tmp
oc exec ${podname} -n moe-gwells-test -- /bin/bash -c 'cp --remove-destination /tmp/2018-MAR-28.sanitized/*.sanitized.csv  /opt/app-root/src/database/code-tables/registries/'
oc exec ${podname} -n moe-gwells-test -- /bin/bash -c 'export PGPASSWORD=$DATABASE_PASSWORD;cd /opt/app-root/src/database/code-tables/registries/;psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  << EOF
\i clear-tables.sql
\ir ../../scripts/registries/populate-xforms-registries.sql
\i data-load-static-codes.sql
\ir ../../scripts/registries/populate-registries-from-xform.sql
\ir ../../scripts/registries/post-deploy.sql
EOF
'
