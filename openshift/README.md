# Openshift Configuration and Notes

GWELLS runs on the BC Gov Pathfinder OpenShift cluster with deployments and resources spanning 4 projects.

## Projects/Namespaces

`moe-gwells-tools` houses the Jenkins-based CI/CD system, which runs pipelines using the Jenkinsfile in the root of this repository.  Builds and images are also located in this project (when an image is ready to be deployed to an environment, it is tagged across to that environment's project).

`moe-gwells-dev` is where developer environments live.  There is generally one active environment/deployment in this project per pull request.  Active environments are deployed at a URL in the form of https://gwells-dev-pr-999.pathfinder.gov.bc.ca/gwells/.

* note: resources for each pull request environment are grouped by the "app" label. For example, you can select all resources for PR 999 using the label selector `-l app=gwells-dev-pr-999`. These resources are cleaned up by Jenkins when the pull request is merged or closed.

`moe-gwells-test` is where **test** and **demo** environments are located.  Staging is automatically deployed when a pull request is made against the `master` branch (and the version deployed at staging can optionally be deployed to production).  To deploy to the *demo* environment, make a pull request against the `demo` branch.

`moe-gwells-prod` is where the production environment is located.

## CI/CD Pipeline

The Jenkins CI/CD pipeline is designed to roll out a new version of the GWELLS application from dev to staging to production automatically. It uses the Jenkinsfile in the repo root and OpenShift tools to build the app from source and deploy the image.

The CI/CD pipeline functions by having Jenkins monitor GitHub pull requests.

### Deploy to a dev environment

When a pull request is made against the `release` branch, a dev environment will be created for the pull request, which should mirror the production environment as closely as is practical. Closing the pull request cleans up the dev environment.

### Deploy to staging

When a pull request is merged into release, the release pipeline will re-build the `release` branch into a new application image and deploy it to staging. This process relies on having a `release` -> `master` pull request open.

### Deploy to production

Use the Jenkins pipeline to approve the deployment of an image in staging to production. The staging image will be tagged as the latest production image and production will be redeployed.


## Prerequisites to deploying to staging/production

The application will roll itself out to staging and production automatically using the Jenkinsfile. However, if starting from a brand new, empty environment, some resources and backing services need to be deployed first:

#### Prerequisite images

The database image comes from bcgov/postgresql-oracle_fdw. Ensure this image is present and can be pulled into the tools project.

#### ConfigMaps and Secrets

ConfigMaps and Secrets must be created for each environment. The Jenkinsfile is set up to make a copy of the following "base" objects for each environment (see the file in parentheses for keys/values that are required):

* ConfigMaps:
  * `gwells-global-config` (backend.dc.json)

* Secrets:
  * `gwells-minio-secrets` (backend.dc.json)
  * `gwells-django-secrets` (backend.dc.json)
  * `gwells-database-secrets` (postgresql.dc.yml)

#### Minio object storage

Private object storage is provided by a minio service, but minio is not currently deployed as part of the pipeline.  Please see `openshift/minio.dc.json` for a deployment config template.

#### Minio backup 

A backup cronjob is deployed by the pipeline, but the BuildConfig needs to be created once before running the pipeline.  Please see `openshift/jobs/minio-backup`. Apply the BuildConfig template and then `oc tag` the resulting image to the project where backups will run. This only needs to be done once.


## Data migration

Data will have to be migrated to the database running on OCP4.


The following was tested for staging:
* ensure `ftw_reader` user is in place (for tile server).  Must have connect privileges.
* `pg_dump -d gwells -Fp -c -C -f /tmp/backup/staging-20201208.sql --exclude-table=spatial_ref_sys`
* rsync to OCP4 (todo: automate this step)
* `psql -x -v ON_ERROR_STOP=1 2>&1 < staging-20201208.sql`
