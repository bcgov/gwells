# How to configure a CI/CD pipeline for GWELLS on OpenShift

- Create a project to house the Jenkins instance that will be responsible for promoting application images (via OpenShift ImageStreamTags) across environment; the exact project name used was "moe-gwells-tools".
- Create the BuildConfiguration within this project using the ```oc``` command and "gwells-build.json" file:

```
oc process -f gwells-build.json | oc create -f -
```

This build config is in the openshift namespace as it uses the Python 3.5 S2I strategy.


- Deploy a Jenkins instance with persistent storage into the tools project (moe-gwells-tools) using the web gui
  - Install the promoted builds plugin
  - Install the GitHub plugin
  - Install the Environment Injector plugin
- Configure a job that has an OpenShift ImageStream Watcher as its SCM source and promotion states for each environment
- In each promotion configuration, tag the target build's image to the appropriate promotion level; this was done using a shell command because the OpenShift plugins do not appear to handle parameter subsitution inside promotions properly.
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
Create a webhook for the push event only to Payload URL:  https://jenkins-moe-gwells-tools.pathfinder.gov.bc.ca/github-webhook/
Content type: application/json

 
- Deploy a Postgresql database instance with persistent storage into the project environment using the web gui and postgresql-presistent template
- Leave the Namespace set to openshift and set the PostgreSQL Database Name to gwells
- Use the JSON file in this directory  and `oc` tool to create the necessary app resources within each project (user and password can be found in the postgresql deployment environment variables in the web gui):

```
oc process -f gwells-app-environment.json -v DATABASE_USER=<user> -v DATABASE_PASSWORD=<password> -v APP_DEPLOYMENT_TAG=<tag> | oc create -f -
```

Where APP_DEPLOYMENT_TAG used is dev, test, prod as set up in Jenkins instance.
The deployment config uses the moe-gwells-tools namespace since that is where the image stream resides.


# How to access Jenkins for gwells

- Login to https://jenkins-moe-gwells-tools.pathfinder.gov.bc.ca with the username/password that was provided to you.

# How to access OpenShift for gwells

## Web UI
- Login to https://console.pathfinder.gov.bc.ca:8443; you'll be prompted for GitHub authorization.

## Command-line (```oc```) tools
- Download OpenShift [command line tools](https://github.com/openshift/origin/releases/download/v1.2.1/openshift-origin-client-tools-v1.2.1-5e723f6-mac.zip), unzip, and add ```oc``` to your PATH.  
- Copy command line login string from https://console.pathfinder.gov.bc.ca:8443/console/command-line.  It will look like ```oc login https://console.pathfinder.gov.bc.ca:8443 --token=xtyz123xtyz123xtyz123xtyz123```
- Paste the login string into a terminal session.  You are now authenticated against OpenShift and will be able to execute ```oc``` commands. ```oc -h``` provides a summary of available commands.



# Background reading/Resources

[Free OpenShift book](https://www.openshift.com/promotions/for-developers.html) from RedHat – good overview

[Red Hat Container Development Kit](http://developers.redhat.com/products/cdk/overview/)

# OpenShift CI/CD pieline Demos:

- https://www.youtube.com/watch?v=65BnTLcDAJI
- https://www.youtube.com/watch?v=wSFyg6Etwx8


  

   
