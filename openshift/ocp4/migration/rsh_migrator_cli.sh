#!/bin/bash
MIGRATOR_POD=$(oc get pods -n "$1" | grep "migrator-cli" | grep Running | head -1 | awk '{print $1}')
echo "oc rsh -n $1 $MIGRATOR_POD /bin/bash"
oc rsh -n "$1" "$MIGRATOR_POD" /bin/bash