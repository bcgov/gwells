#!/bin/bash
# Usage: ./migrate_minio.sh [test/prod]

# This script connects to minio on pathfinder and runs `mc mirror` to the silver minio alias

# Get variables from previous scripts or params
ENVIRONMENT=${ENVIRONMENT:-$1}
. ./params.sh
. ./require_pathfinder_auth.sh

# Start minio migration
GWELLS_MINIO_POD=$(oc --kubeconfig="$KUBECONFIG" get pods -n "$NAMESPACE" | grep "gwells-minio" | head -1 | awk '{print $1}')
echo "------------------------------------------------------------------------------"
echo "Found pod $GWELLS_MINIO_POD on $NAMESPACE"
echo "Starting minio client (mc) mirror..."
echo "------------------------------------------------------------------------------"


# Run mc mirror
# Note: The options --remove and --overwrite are there so we can be sure we copy the right data
SECONDS=0
# The .minio.sys folder causes issues when doing mc mirror, so let's delete it.
# It contains metadata and it won't affect your data.
oc --kubeconfig="$KUBECONFIG" exec -n "$NAMESPACE" "$GWELLS_MINIO_POD" -- bash -c "if [ -d /opt/minio/s3/data/.minio.sys ];then rm -rf /opt/minio/s3/data/.minio.sys; fi"
oc --kubeconfig="$KUBECONFIG" exec -n "$NAMESPACE" "$GWELLS_MINIO_POD" -- bash -c "/opt/minio/mc -C /opt/minio/.mc mirror --remove --overwrite /opt/minio/s3/data/ silver/"
duration=$SECONDS
# Sanity check
oc --kubeconfig="$KUBECONFIG" exec -n "$NAMESPACE" "$GWELLS_MINIO_POD" -- bash -c "/opt/minio/mc -C /opt/minio/.mc diff /opt/minio/s3/data/ silver/" |& tee /tmp/mc_diff.log
echo "------------------------------------------------------------------------------"
echo "Minio mirror took $((duration / 60)) minutes and $((duration % 60)) seconds."
echo "Please check the mc diff result (/tmp/mc_diff.log)"
echo "------------------------------------------------------------------------------"

