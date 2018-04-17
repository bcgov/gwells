# Openshift Configuration and Notes

## Resource Limits

moe-gwells-dev has a resource limit of [8 cores](https://console.pathfinder.gov.bc.ca:8443/console/project/moe-gwells-dev/quota) which is enough for all pods to run, but may not be enough to deploy (both [developer](https://console.pathfinder.gov.bc.ca:8443/console/project/moe-gwells-tools/browse/pipelines/gwells-pipeline-developer?tab=history) and [master](https://console.pathfinder.gov.bc.ca:8443/console/project/moe-gwells-tools/browse/pipelines/gwells-pipeline?tab=history) pipelines.)

Deployments may fail without a meaningful error message (e.g. timeout is the most common one).  If this happens then we scale down all ancillary pods in [moe-gwells-dev](https://console.pathfinder.gov.bc.ca:8443/console/project/moe-gwells-dev/overview) or [moe-gwells-test](https://console.pathfinder.gov.bc.ca:8443/console/project/moe-gwells-test/overview).  This does not seem to happon on [moe-gwells-prod](https://console.pathfinder.gov.bc.ca:8443/console/project/moe-gwells-prod/overview).

A more detailed explanation is that each application has its own limit (e.g. [DEV gwells](https://console.pathfinder.gov.bc.ca:8443/console/project/moe-gwells-dev/set-limits?kind=DeploymentConfig&name=gwells) has CPU 700 millicores available while running) but during deployment, may require MORE than the 700 millicores during deployments.

Until we can fine-tune each individual applications CPU limit, or are provided more resources overall, we need to be watchful for failed deployments due to running out of resources.   To fix this, we get ready to rerun the pipeline but before that, we go to the [Overview page](https://console.pathfinder.gov.bc.ca:8443/console/project/moe-gwells-dev/overview) expand the view into each of the applications in turn and scale down to 0:
- metabase
- schema-spy
- sparx-ea-gwells

We try the pipline again and if it still fails, we also scale down:
- gwells-minio
- proxy-caddy

IMPORTANT: Scale these applications back up to their original # of pods, so that day-to-day work (e.g. working with data architects) can still continue.