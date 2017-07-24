# How to configure a CI/CD pipeline for GWELLS on OpenShift

- Create a project to house the Jenkins instance that will be responsible for promoting application images (via OpenShift ImageStreamTags) across environment; the exact project name used was "moe-gwells-tools".

```
oc add-project moe-gwells-tools
```
- Create the objects needed to form the build pipeline within this project using the ```oc``` command and "gwells-build.json" file:

```
oc process -f gwells-build.json | oc create -f -
```

The gwells-build.json template file contains the following objects:

- Build Configuration for the gwells Python 3.5 S2I build
- Build Configuration for the OpenShift Pipeline that runs the build
- Deployment Configuration for a Postgres database used by SonarQube
- Persistent volume for the above Postgres database
- A Deployment Configuration for SonarQube
- Persistent volume for the above SonarQube instance

Note that when the above objects are added to the "moe-gwells-tools" namespace, and the Pipeline is run for the first time, OpenShift will automatically create a Jenkins Pipeline deployment.

Obtain the credentials for this Pipeline deployment by viewing the Environment properties of the Jenkins Pipeline deployment.

Login to the Jenkins instance by clicking on the appropriate link in the Routes tab, a username of admin and the password found above.

Perform the following steps:

- Click on Manage Jenkins, and then Configure Jenkins.  
- Scroll down to the Jenkins Location section, and adjust the setting for Jenkins URL to match the actual URL for Jenkins.
- Scroll down to the Jenkins Location section, and adjust the setting for Jenkins URL to match the actual URL for Jenkins.

- In the OpenShift Builder section, increase the Build timeout to match typical build times for your application.  For example you may need to increase the build time to 1800 if the build time is 30 minutes.

- In the Cloud section, adjust the maven image so that it has an increased Memory Limit.  Note that you will need to click the Advanced button to show the Memory Limit section.  A limit of 2Gi is recommended in order for SonarQube to run properly.

- Create an OpenShift project for each "environment" (e.g. DEV, TEST, PROD); Exact names used were moe-gwells-dev, moe-gwells-test, moe-gwells-prod
- Configure the access controls to allow the Jenkins instance to tag imagestreams in the environment projects, and to allow the environment projects to pull images from the tools project:
 
```
oc policy add-role-to-user system:image-puller system:serviceaccount:moe-gwells-dev:default -n moe-gwells-tools
oc policy add-role-to-user edit system:serviceaccount:moe-gwells-tools:default -n moe-gwells-dev

oc policy add-role-to-user system:image-puller system:serviceaccount:moe-gwells-test:default -n moe-gwells-tools
oc policy add-role-to-user edit system:serviceaccount:moe-gwells-tools:default -n moe-gwells-test

oc policy add-role-to-user system:image-puller system:serviceaccount:moe-gwells-prod:default -n moe-gwells-tools
oc policy add-role-to-user edit system:serviceaccount:moe-gwells-tools:default -n moe-gwells-prod
```


In the GitHub repository go to Settings > Webhooks > Add webhook
Create a webhook for the push event only to Payload URL specified in the OpenShift Console at: Edit Build Config gwells-pipeline > Triggers > Github webhooks
Content type: application/json

 
- Deploy a Postgresql database instance with 2G persistent storage and 1G Memory, into the project environment using the web gui and postgresql-presistent template
- Leave the Namespace set to openshift and set the PostgreSQL Database Name to gwells
- Use the JSON file in this directory  and `oc` tool to create the necessary app resources within each project (user and password can be found in the postgresql deployment environment variables in the web gui):

```
oc project <projectname>
oc process -f gwells-app-environment.json -v DATABASE_USER=<user> -v DATABASE_PASSWORD=<password> -v APP_DEPLOYMENT_TAG=<tag> -v APPLICATION_DOMAIN=gwells-<tag>.pathfinder.gov.bc.ca | oc create -f -
```

Where APP_DEPLOYMENT_TAG used is dev, test, prod as set up in Jenkins instance.
The deployment config uses the moe-gwells-tools namespace since that is where the image stream resides.


# How to access Jenkins for GWELLS

- Login to https://jenkins-pipeline-svc-moe-gwells-tools.pathfinder.gov.bc.ca with the username/password that was provided to you.

# How to access OpenShift for GWELLS

## Web UI
- Login to https://console.pathfinder.gov.bc.ca:8443; you'll be prompted for GitHub authorization.

## Command-line (```oc```) tools
- Download OpenShift [command line tools](https://github.com/openshift/origin/releases/download/v1.5.1/openshift-origin-client-tools-v1.5.1-7b451fc-windows.zip), unzip, and add ```oc``` to your PATH.  
- Copy command line login string from https://console.pathfinder.gov.bc.ca:8443/console/command-line.  It will look like ```oc login https://console.pathfinder.gov.bc.ca:8443 --token=xtyz123xtyz123xtyz123xtyz123```
- Paste the login string into a terminal session.  You are now authenticated against OpenShift and will be able to execute ```oc``` commands. ```oc -h``` provides a summary of available commands.



# Background reading/Resources

[Free OpenShift book](https://www.openshift.com/promotions/for-developers.html) from RedHat – good overview

[Red Hat Container Development Kit](http://developers.redhat.com/products/cdk/overview/)



  

   
