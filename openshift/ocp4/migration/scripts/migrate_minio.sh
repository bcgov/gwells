#!/bin/bash
# This script connects to minio on pathfinder and runs `mc mirror` to the silver minio alias

# Get variables from previous scripts or params
NAMESPACE=${NAMESPACE:-$1}
KUBECONFIG=${KUBECONFIG:-'/tmp/KUBECONFIG'}

if [[ -z "$NAMESPACE" ]]; then
  echo "Namespace not set, exiting... (input param1 moe-gwells-[test/prod])"
  exit 1
fi

if [ ! -f "$KUBECONFIG" ]; then
  read -r -p "Enter Pathfinder auth token: " AUTH_TOKEN
  oc --kubeconfig="$KUBECONFIG" login https://console.pathfinder.gov.bc.ca:8443 --token="$AUTH_TOKEN"
fi

# Start minio migration
GWELLS_MINIO_POD=$(oc --kubeconfig="$KUBECONFIG" get pods -n "$NAMESPACE" | grep "gwells-minio" | head -1 | awk '{print $1}')
echo "------------------------------------------------------------------------------"
echo "Found pod $GWELLS_MINIO_POD on $NAMESPACE"
echo "Starting minio client (mc) mirror..."
echo "------------------------------------------------------------------------------"


# Run mc mirror
# Note: The options --remove and --overwrite are there so we can be sure we copy the right data
SECONDS=0
oc --kubeconfig="$KUBECONFIG" exec -n "$NAMESPACE" "$GWELLS_MINIO_POD" -- bash -c "/opt/minio/mc -C /opt/minio/.mc mirror --remove --overwrite /opt/minio/s3/data/ silver/"
duration=$SECONDS
# Sanity check
oc --kubeconfig="$KUBECONFIG" exec -n "$NAMESPACE" "$GWELLS_MINIO_POD" -- bash -c "/opt/minio/mc -C /opt/minio/.mc diff /opt/minio/s3/data/ silver/" |& tee /tmp/mc_diff.log
echo "------------------------------------------------------------------------------"
echo "Minio mirror took $((duration / 60)) minutes and $((duration % 60)) seconds."
echo "Please check the mc diff result (/tmp/mc_diff.log)"
echo "------------------------------------------------------------------------------"
