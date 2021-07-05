#!/bin/bash
# Usage:  ./activate-proxy.sh [test/prod]

# add --revert to end (after test/prod argument) to switch the routes back to OCP3 services.
# i.e. ./activate_proxy.sh [test/prod] --revert

# Get variables from previous scripts or params
ENVIRONMENT=${ENVIRONMENT:-$1}
. ./params.sh "$ENVIRONMENT"
. ./require_pathfinder_auth.sh

set -euo pipefail

echo
echo "Switching main GWELLS route to forward requests to OCP4  ($NAMESPACE ; env: $POD_SUFFIX)"
echo


ROUTE_PATCH=$(cat <<-EOF
{
	"spec": {
		"port": {
			"targetPort": "2015-tcp"
		},
		"to": {
			"kind": "Service",
			"name": "gwells-maintenance-${POD_SUFFIX}"
		}
	}
}
EOF
)

REVERT_ROUTE_PATCH_GWELLS=$(cat <<-EOF
{
	"spec": {
		"port": {
			"targetPort": "web"
		},
		"to": {
			"kind": "Service",
			"name": "gwells-${POD_SUFFIX}"
		}
	}
}
EOF
)

REVERT_ROUTE_PATCH_TILESERV=$(cat <<-EOF
{
	"spec": {
		"port": {
			"targetPort": 8080
		},
		"to": {
			"kind": "Service",
			"name": "pgtileserv-${POD_SUFFIX}"
		}
	}
}
EOF
)

if echo $* | grep -e "--revert" -q
then
	# use revert script
	oc --kubeconfig="$KUBECONFIG" -n "$NAMESPACE" patch "route/gwells-$POD_SUFFIX" -p "$REVERT_ROUTE_PATCH_GWELLS"
	oc --kubeconfig="$KUBECONFIG" -n "$NAMESPACE" patch "route/pgtileserv-$POD_SUFFIX" -p "$REVERT_ROUTE_PATCH_TILESERV"
	echo
	echo "route/gwells-$POD_SUFFIX patched to direct traffic to OCP3 services (proxy to ocp4 disabled)"
	echo
else
	oc --kubeconfig="$KUBECONFIG" -n "$NAMESPACE" patch "route/gwells-$POD_SUFFIX" -p "$ROUTE_PATCH"
	oc --kubeconfig="$KUBECONFIG" -n "$NAMESPACE" patch "route/pgtileserv-$POD_SUFFIX" -p "$ROUTE_PATCH"

	echo
	echo "route/gwells-$POD_SUFFIX patched to direct traffic to OCP4 proxy"
	echo
fi


# switch to service gwells-maintenance-staging / gwells-maintenance-production ; target port: 2015-tcp

