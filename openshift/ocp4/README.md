# OpenShift 4 Deployment

## Prerequisites

The Jenkins pipeline is designed to roll out GWELLS to dev, test and prod.  Before beginning, it requires a Jenkins deployment,
Python, PostGIS, Minio, and pg_tileserv base images, and secrets in every namespace before it can run. The pipeline should roll everything else out.


### Jenkins
Note: See https://developer.gov.bc.ca/Cloud-Migration/Migrating-Your-BC-Gov-Jenkins-to-the-Cloud for background info on Jenkins in the OCP4 cluster.

* Build the `jenkins-basic` provided in the above link. Ensure that the image has been outputted to the jenkins-basic imagestream in the tools project.
* Use `oc process` to process the Jenkins templates in `/openshift/ocp4/jenkins`. The same container image (built in step 1) can be used for both the primary and secondary. There are required parameters such as the Jenkins host name.
* Log in to Jenkins.  Note the URL in the OpenShift Networking > Routes menu, or by using `oc get routes -o wide`.
* Add GitHub credentials to Jenkins. Use type `username/password`, with a GitHub token as the password.  The `bcgov-csnr-cd` account can be used.
* Set up a Multibranch Pipeline for GWELLS. Ensure that only PRs from origin are accepted (no forks).  If accepting forks, ensure that only forks from
users with write access to the repo are allowed.

### Base images

#### Python

GWELLS uses a base image `ubi8/python-38` with GDAL installed.  Since installing GDAL can take some time, it is not re-built and re-installed for every
pipeline run.  The image should be built before running the pipeline. Other python packages will be installed during normal pipeline runs.

The repo contains the BuildConfig used to build the base container image.  In the `openshift/ocp4/docker/backend` directory, run `oc4 apply -f gwells-python.bc.yaml -n 26e83e-tools`. Start the build with `oc start-build`.

#### PostgreSQL/PostGIS

GWELLS uses PostgreSQL with the PostGIS extension. Import the Crunchy Data PostGIS image with `oc import-image --from=crunchydata/crunchy-postgres-gis:centos7-12.5-3.0-4.5.1` (check the repository at https://hub.docker.com/r/crunchydata/crunchy-postgres-gis/
for an appropriate tag). 

Use `oc tag -n 26e83e-tools crunchy-postgres-gis:centos7-12.5-3.0-4.5.1 26e83e-dev:crunchy-postgres-gis:centos7-12.5-3.0-4.5.1` to copy the image into the dev, test and prod namespaces (note the `26e83e-dev` image namespace in the second argument - repeat for dev, test and prod).  This procedure allows importing a new version of the database image into the tools namespace without affecting existing environments, and then progressively testing it on dev and test before making it available to production. 

#### Minio

Import the minio image into the tools repo using `oc import-image --from=minio/minio` (check https://hub.docker.com/r/minio/minio/). At this time the image need only be available in the tools namespace.

#### pg_tileserv

Import the pg_tileserv image into the tools repo using `oc import-image --from=pramsey/pg_tileserv` (check https://hub.docker.com/r/pramsey/pg_tileserv/ for the most up to date tag). At this time the image need only be available in the tools namespace.

### image-puller roles

The dev, test and prod namespace service accounts will need image pull roles.
Use `oc -n 26e83e-tools policy add-role-to-group system:image-puller system:serviceaccounts:26e83e-dev` (note namespace at end- repeat for test and prod).

### Secrets / ConfigMaps

The following secrets / configmaps need to be deployed to each environment namespace (dev/test/prod):
| name | kind |
| gwells-django-secrets| Secret |
| gwells-database-secrets | Secret |
| gwells-e-licensing-secrets| Secret |
| gwells-minio-secrets | Secret |
| gwells-global-config | ConfigMap |

These objects hold base/default config for each namespace. The Jenkins pipeline makes copies of these as (e.g.) `gwells-django-dev-pr-1110` or `gwells-django-prod` (depending on environment).

### NetworkSecurityPolicies

We need to create NetworkSecurityPolicy objects to define the rules for external and internal network communication.

As a short term fix (for migration), there are NetworkSecurityPolicies that mimic the OCP3 cluster.

```
oc apply -f openshift/ocp4/jenkins/jenkins.nsp.yaml -p NAMESPACE=<namespace> | oc apply -n <namespace> -f -
```

### Backup jobs

Unlike OCP3, where an NFS storage volume had to be manually provisioned, we can self-provision backup storage using the storage class `netapp-file-backup`.  The Jenkinsfile has been updated to provision a volume for the minio and postgres backups to write to.
