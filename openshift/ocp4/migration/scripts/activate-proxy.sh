#!/bin/bash

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

# switch to service gwells-maintenance-staging / gwells-maintenance-production ; target port: 2015-tcp

oc --kubeconfig=/tmp/KUBECONFIG -n "$NAMESPACE" patch "route/gwells-$ENV_NAME" -p "$ROUTE_PATCH"

echo
echo "route/gwells-$ENV_NAME patched to direct traffic to OCP4 proxy"
echo
