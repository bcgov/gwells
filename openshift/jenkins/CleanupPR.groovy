// note: a copy of this file lives in Jenkins config. We need a way to update the Jenkins config 
// when changes are made to this file.

import groovy.json.JsonSlurper

String TOOLS_PROJECT = "moe-gwells-tools"
String DEV_PROJECT = "moe-gwells-dev"

def jsonSlurper = new JsonSlurper()

// the webhook trigger comes from GitHub as a POST request with a "payload" object in the body
String ghEventType = build.buildVariableResolver.resolve("x_github_event")
def payload = jsonSlurper.parseText(build.buildVariableResolver.resolve("payload"))
def prNum = payload['number']


// this script is triggered on all events, but we are specifically interested in pull requests that are closed
// pull requests come with actions like "opened", "closed".  Merged and closed are the same event (there is an
// additional "merged: true" property)
if (ghEventType == 'pull_request' && payload['action'] == 'closed' && prNum) {

    def sout = new StringBuilder(), serr = new StringBuilder()

    // delete all the objects in the DEV namespace labeled with this PR number
    // todo: there are several labels that need to be targeted and hardcoding them is fragile.
    // a future task should focus on creating a label that applies to all resources associated with one pull request.
    def deleteAllAppObjects = "oc delete all,pvc,secret,configmap -n ${DEV_PROJECT} -l app=gwells-dev-pr-${prNum} -l appver=gwells-dev-pr-${prNum} -l gluster.kubernetes.io/provisioned-for-pvc=gwells-pgsql-dev-pr-${prNum}".execute()
    deleteAllAppObjects.consumeProcessOutput(sout, serr)
    deleteAllAppObjects.waitForOrKill(5000)
    println "out> $sout err> $serr"

    // delete the objects in the tools project (this is primarly the build configs,
    // the imagestream is not unique to each pull request).
    sout = new StringBuilder()
    serr = new StringBuilder()
    def deleteAllBuilds = "oc delete all -n ${TOOLS_PROJECT} -l appver=gwells-dev-pr-${prNum}".execute()
    deleteAllBuilds.consumeProcessOutput(sout, serr)
    deleteAllBuilds.waitForOrKill(5000)
    println "out> $sout err> $serr"

    // untag the images tagged with this PR number
    sout = new StringBuilder()
    serr = new StringBuilder()
    def untagImages = "oc tag -d gwells-application:pr-${prNum}".execute()
    untagImages.consumeProcessOutput(sout, serr)
    untagImages.waitForOrKill(5000)
    println "out> $sout err> $serr"
    
}
