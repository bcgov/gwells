#!/bin/bash
# Usage:  ./activate-proxy.sh <test|prod>
# add --revert to end (after test/prod argument) to switch the routes back to OCP3 services.


set -euo pipefail

NAMESPACE="moe-gwells-$1"
ENV_NAME="staging"

if [ "$1" == 'prod' ]; then
    ENV_NAME='production'
fi
echo
echo "Switching main GWELLS route to forward requests to OCP4  ($NAMESPACE ; env: $ENV_NAME)"
echo


ROUTE_PATCH=$(cat <<-EOF
{
	"spec": {
		"port": {
			"targetPort": "2015-tcp"
		},
		"to": {
			"kind": "Service",
			"name": "gwells-maintenance-${ENV_NAME}"
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
			"name": "gwells-${ENV_NAME}"
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
			"name": "pgtileserv-${ENV_NAME}"
		}
	}
}
EOF
)

if echo $* | grep -e "--revert" -q
then
	# use revert script
	oc --kubeconfig=/tmp/KUBECONFIG -n "$NAMESPACE" patch "route/gwells-$ENV_NAME" -p "$REVERT_ROUTE_PATCH_GWELLS"
	oc --kubeconfig=/tmp/KUBECONFIG -n "$NAMESPACE" patch "route/pgtileserv-$ENV_NAME" -p "$REVERT_ROUTE_PATCH_TILESERV"
	echo
	echo "route/gwells-$ENV_NAME patched to direct traffic to OCP3 services (proxy to ocp4 disabled)"
	echo
else
	oc --kubeconfig=/tmp/KUBECONFIG -n "$NAMESPACE" patch "route/gwells-$ENV_NAME" -p "$ROUTE_PATCH"
	oc --kubeconfig=/tmp/KUBECONFIG -n "$NAMESPACE" patch "route/pgtileserv-$ENV_NAME" -p "$ROUTE_PATCH"

	echo
	echo "route/gwells-$ENV_NAME patched to direct traffic to OCP4 proxy"
	echo
fi


# switch to service gwells-maintenance-staging / gwells-maintenance-production ; target port: 2015-tcp

