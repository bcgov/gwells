package bcgov

import org.kohsuke.github.*
import org.jenkinsci.plugins.workflow.cps.CpsScript
import com.cloudbees.jenkins.GitHubRepositoryName

/*
* Reference:
*   - http://github-api.kohsuke.org/apidocs/index.html
*   - https://github.com/jenkinsci/github-plugin/blob/master/src/main/java/com/cloudbees/jenkins/GitHubRepositoryName.java
* */
class GitHubHelper {

    static String getRepositoryUrl(CpsScript script){
        return script.scm.getUserRemoteConfigs()[0].getUrl()
    }

    static GHRepository getGitHubRepository(CpsScript script){
        return getGitHubRepository(script.scm.getUserRemoteConfigs()[0].getUrl())
    }

    @NonCPS
    private static String stackTraceAsString(Throwable t) {
        StringWriter sw = new StringWriter();
        t.printStackTrace(new PrintWriter(sw));
        return sw.toString()
    }

    @NonCPS
    static GHRepository getGitHubRepository(String url){
        return GitHubRepositoryName.create(url).resolveOne()
    }

    static GHPullRequest getPullRequest(CpsScript script){
        return getGitHubRepository(script).getPullRequest(Integer.parseInt(script.env.CHANGE_ID))
    }

    static String getPullRequestLastCommitId(CpsScript script){
        return getPullRequest(script).getHead().getSha()
    }

    @NonCPS
    static boolean mergeAndClosePullRequest(String repositoryUrl, int prNumber, String mergeMethod){
        GHRepository repo=getGitHubRepository(repositoryUrl)
        GHPullRequest pullRequest = repo.getPullRequest(prNumber)
        Boolean mergeable = pullRequest.getMergeable()
        GHIssueState state = pullRequest.getState()
        boolean ret=false
        boolean doClose=true;

        if (state != GHIssueState.CLOSED) {
            GHCommitPointer head = pullRequest.getHead()
            if (!pullRequest.isMerged()) {
                if (mergeable != null && mergeable.booleanValue() == true) {
                    pullRequest.merge("Merged PR-${prNumber}", head.getSha(), GHPullRequest.MergeMethod.valueOf(mergeMethod.toUpperCase()))
                } else {
                    doClose = false
                }
            }

            if (doClose && pullRequest.getRepository().getFullName().equalsIgnoreCase(head.getRepository().getFullName())) {
                if (head.getRef() != null) {
                    GHRef headRef = repo.getRef('heads/' + head.getRef())
                    if (headRef != null) {
                        headRef.delete()
                    }
                }
            }

            if (doClose){
                pullRequest.close()
                ret = true
            }
        }else{
            ret = true
        }

        return ret
    }
    static boolean mergeAndClosePullRequest(CpsScript script) {
        return mergeAndClosePullRequest(script, 'merge')
    }
    static boolean mergeAndClosePullRequest(CpsScript script, String mergeMethod) {
        try {
            return mergeAndClosePullRequest(getRepositoryUrl(script), Integer.parseInt(script.env.CHANGE_ID), mergeMethod)
        }catch (ex){
            //This need to be done because the github API does NOT return serializable Exceptions
            script.echo "Original Stack Trace:\n${stackTraceAsString(ex)}"
            throw new IOException(ex.message)
        }
    }

    static void commentOnPullRequest(CpsScript script, String comment) {
        try {
            commentOnPullRequest(getRepositoryUrl(script), Integer.parseInt(script.env.CHANGE_ID), comment)
        }catch (ex){
            //This need to be done because the github API does NOT return serializable Exceptions
            script.echo "Original Stack Trace:\n${stackTraceAsString(ex)}"
            throw new IOException(ex.message)
        }
    }

    @NonCPS
    static void commentOnPullRequest(String repositoryUrl, int pullRequestNumber, String comment) {
        GHRepository repo=getGitHubRepository(repositoryUrl)
        GHPullRequest pullRequest = repo.getPullRequest(pullRequestNumber)
        pullRequest.comment(comment)

    }

    static GHDeploymentBuilder createDeployment(CpsScript script, String ref) {
        return getGitHubRepository(script).createDeployment(ref)
    }


    static GHDeploymentBuilder createDeployment(String url, String ref) {
        return getGitHubRepository(url).createDeployment(ref)
    }

    static def createDeploymentStatus(CpsScript script, long deploymentId, GHDeploymentState state) {
        return getGitHubRepository(script).getDeployment(deploymentId).createStatus(state)
    }

    /*
    * http://github-api.kohsuke.org/apidocs/org/kohsuke/github/GHDeploymentBuilder.html
    * */
    @NonCPS
    def createDeployment(String url, String ref, Map deploymentConfig) {
        //long deploymentId = -1
        GHRepository repository=getGitHubRepository(url)

        /*
        for (GHDeployment deployment:repository.listDeployments(null, ref, null, deploymentConfig.environment)){
            deployment.createStatus(GHDeploymentState.PENDING).create()
            return deployment.getId()
        }
        */
        GHDeploymentBuilder builder=repository.createDeployment(ref)
        builder.environment(deploymentConfig.environment)
        builder.autoMerge(false)
        builder.requiredContexts([])


        //deployment=null

        if (deploymentConfig!=null) {
            //if (deploymentConfig.environment) {
            //    builder.environment(deploymentConfig.environment)
            //}

            if (deploymentConfig.payload) {
                builder.payload(deploymentConfig.payload)
            }

            if (deploymentConfig.description) {
                builder.description(deploymentConfig.description)
            }

            if (deploymentConfig.task) {
                builder.task(deploymentConfig.task)
            }

            if (deploymentConfig.requiredContexts) {
                builder.requiredContexts(deploymentConfig.requiredContexts)
            }
        }

        /*
        long deploymentId = builder.create().getId()
        builder=null;
        return deploymentId
        */

        return builder.create().getId()
    }

    long createDeployment(CpsScript script, String ref, Map deploymentConfig) {
        script.echo "ref:${ref} - config:${deploymentConfig}"
        return createDeployment(script.scm.getUserRemoteConfigs()[0].getUrl(), ref, deploymentConfig)
    }

    @NonCPS
    static long createDeploymentStatus(String url, long deploymentId, String statusName, Map deploymentStatusConfig) {
        def ghRepo=getGitHubRepository(url)
        def ghDeploymentState=GHDeploymentState.valueOf(statusName)

        def ghDeploymentStatus=ghRepo.root.retrieve().to(ghRepo.getApiTailUrl("deployments/")  + deploymentId, GHDeployment.class).wrap(ghRepo).createStatus(ghDeploymentState)

        if (deploymentStatusConfig.description){
            ghDeploymentStatus.description(deploymentStatusConfig.description)
        }
        if (deploymentStatusConfig.targetUrl){
            ghDeploymentStatus.targetUrl(deploymentStatusConfig.targetUrl)
        }
        return ghDeploymentStatus.create().getId()
    }
    static long createDeploymentStatus(CpsScript script, long deploymentId, String statusName, Map config) {
        script.echo "deploymentId:${deploymentId} - status:${statusName} - config:${config}"
        return createDeploymentStatus(script.scm.getUserRemoteConfigs()[0].getUrl(), deploymentId, statusName, config)
    }
    @NonCPS
    static void createCommitStatus(String url, String sha1, String statusName, String targetUrl, String description, String context) {
        def ghRepo=getGitHubRepository(url)
        def ghCommitState=GHCommitState.valueOf(statusName)

        ghRepo.createCommitStatus(sha1, ghCommitState, targetUrl, description, context)
    }

    static void createCommitStatus(CpsScript script, String ref, String statusName, String targetUrl, String description, String context) {
        createCommitStatus(script.scm.getUserRemoteConfigs()[0].getUrl() as String, ref, statusName, targetUrl, description, context)
    }
}
