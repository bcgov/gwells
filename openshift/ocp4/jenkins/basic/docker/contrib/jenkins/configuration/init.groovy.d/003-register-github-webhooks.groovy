import jenkins.*
import jenkins.model.*
import org.kohsuke.github.*


if ('prod'.equalsIgnoreCase(System.getenv('ENV_NAME'))){
    String jenkinsUrl = JenkinsLocationConfiguration.get().getUrl()
    String genericWebHookTriggerToken = Jenkins.instance.getItemByFullName('_SYS/ON_GH_EVENT').getTrigger(org.jenkinsci.plugins.gwt.GenericTrigger.class).getToken()

    Jenkins.instance.getAllItems().each { job ->
        if (job instanceof jenkins.branch.MultiBranchProject){
            try{
                for (def branchSource:job.getSources()){
                if (branchSource instanceof jenkins.branch.BranchSource){
                    if (branchSource.getSource() instanceof org.jenkinsci.plugins.github_branch_source.GitHubSCMSource){
                        def scmBranchSource = branchSource.getSource()
                        //org.jenkinsci.plugins.github_branch_source.GitHubSCMBuilder.uriResolver(job, scmBranchSource.getApiUri())
                        com.cloudbees.plugins.credentials.common.StandardCredentials credentials = org.jenkinsci.plugins.github_branch_source.Connector.lookupScanCredentials(job, scmBranchSource.getApiUri(), scmBranchSource.getCredentialsId())
                        org.kohsuke.github.GitHub github = org.jenkinsci.plugins.github_branch_source.Connector.connect(scmBranchSource.getApiUri(), credentials);
                        String fullName = scmBranchSource.getRepoOwner() + "/" + scmBranchSource.getRepository();
                        //println fullName
                        org.kohsuke.github.GHRepository ghRepository = github.getRepository(fullName);
                        Map hooks =[
                            'github-webhook':['url':"${jenkinsUrl}github-webhook/", 'events':[org.kohsuke.github.GHEvent.PULL_REQUEST, org.kohsuke.github.GHEvent.PUSH]],
                            'generic-webhook-trigger.0':['url':"${jenkinsUrl}generic-webhook-trigger/invoke?token=${genericWebHookTriggerToken}", 'events':[org.kohsuke.github.GHEvent.PULL_REQUEST, org.kohsuke.github.GHEvent.ISSUE_COMMENT]]
                        ]
                        for (def hook:ghRepository.getHooks()){
                            //println hook
                            hooks.each{ String name, Map newHook ->
                                if (hook.getConfig() == null || hook.getConfig()['url'] == null){
                                    println "Something is odd .. a hook in '${fullName}' is null: ${hook}"
                                }else if (hook.getConfig()['url'].startsWith(newHook.url)){
                                    newHook['_hook']=hook
                                }
                            }
                        }
                        //Create Hooks
                        hooks.each{ String name, Map newHook ->
                            Map hookCfg = ['url':newHook.url]
                            if (newHook._hook == null){
                                if (newHook.qs){
                                    if (hookCfg.url.contains('?')){
                                        hookCfg.url=hookCfg.url+'&'
                                    }else{
                                        hookCfg.url=hookCfg.url+'?'
                                    }
                                    hookCfg.url=hookCfg.url+newHook.qs
                                }
                                println "Registering webhook for ${job.name}: ${[new URL(hookCfg.url), newHook.events]}"
                                ghRepository.createHook("web",["url":new URL(hookCfg.url).toExternalForm()], newHook.events,'prod'.equalsIgnoreCase(System.getenv('ENV_NAME')))
                                //ghRepository.createWebHook(new URL(hookCfg.url), newHook.events)
                            }else{
                                println "Webhook already registered for ${job.name}: ${[new URL(hookCfg.url), newHook.events]}"
                            }
                        }
                    }
                }
                } //for
            } catch (ex){
                println "Error registering webhook for ${job.name}"
                println(ex.toString());
                println(ex.getMessage());
                println(ex.getStackTrace()); 
            }
        }
    }
}else{
    println "SKIPPING (Register GitHub WebHooks): Not running in Production mode (ENV_NAME != 'prod') "
}