#!/bin/bash

if [[ -z "$NAMESPACE" ]]; then
  echo "Namespace not set, exiting..." 1>&2
  exit 1
fi

# Find minio pod on pathfinder
GWELLS_MINIO_POD=$(oc --kubeconfig=/tmp/KUBECONFIG get pods -n "$NAMESPACE" | grep "gwells-minio" | head -1 | awk '{print $1}')
echo "------------------------------------------------------------------------------"
echo "Found pod $GWELLS_MINIO_POD on $NAMESPACE"
echo "Starting minio client (mc) mirror..."
echo "------------------------------------------------------------------------------"


# Run mc mirror
# Note - --remove and --overwrite so we can be sure we copy the right data
SECONDS=0
oc --kubeconfig=/tmp/KUBECONFIG exec -n "$NAMESPACE" "$GWELLS_MINIO_POD" -- bash -c "/opt/minio/mc -C /opt/minio/.mc mirror --remove --overwrite /opt/minio/s3/data/ silver/"
duration=$SECONDS
# Sanity check
oc --kubeconfig=/tmp/KUBECONFIG exec -n "$NAMESPACE" "$GWELLS_MINIO_POD" -- bash -c "/opt/minio/mc -C /opt/minio/.mc diff /opt/minio/s3/data/ silver/" |& tee /tmp/mc_diff.log
echo "------------------------------------------------------------------------------"
echo "Minio mirror took $((duration / 60)) minutes and $((duration % 60)) seconds."
echo "Please check the mc diff result (/tmp/mc_diff.log)"
echo "------------------------------------------------------------------------------"

