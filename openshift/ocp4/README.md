# OpenShift 4 Deployment

## Prerequisites

The Jenkins pipeline is designed to roll out GWELLS to dev, test and prod.  However, it requires a Jenkins deployment,
Python, PostGIS, Minio, and pg_tileserv base images, and secrets in every namespace before it can run. The pipeline should roll everything else out.


### Jenkins
Note: See https://developer.gov.bc.ca/Cloud-Migration/Migrating-Your-BC-Gov-Jenkins-to-the-Cloud for background info on Jenkins in the OCP4 cluster.

* Build the `jenkins-basic` provided in the above link. Ensure that the image has been outputted to the jenkins-basic imagestream in the tools project.
* Apply the Jenkins manifests in `/openshift/ocp4/jenkins`. The same image can be used for both the primary and secondary.
* Provide GitHub credentials to Jenkins. Use type `username/password`, with a GitHub token as the password.  The `bcgov-csnr-cd` account can be used.
* Set up a Multibranch Pipeline for GWELLS. Ensure that only PRs from origin are accepted (no forks).  If accepting forks, ensure that only forks from
users with write access to the repo are allowed.

### Base images

#### Python

GWELLS uses a base image `ubi8/python-38` with GDAL installed.  Since installing GDAL can take some time, it is not re-built and re-installed for every
pipeline run.  The image should be built before running the pipeline. Other python packages will be installed during normal pipeline runs.

In the `openshift/ocp4/docker/backend` directory, run `oc4 apply -f gwells-python.bc.yaml -n 26e83e-tools`. Start the build with `oc start-build`.

#### PostgreSQL/PostGIS

#### Minio

#### pg_tileserv
