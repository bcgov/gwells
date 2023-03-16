import com.cloudbees.plugins.credentials.impl.*;
import com.cloudbees.plugins.credentials.*;
import com.cloudbees.plugins.credentials.domains.*;
import org.jenkinsci.plugins.plaincredentials.impl.*;
import jenkins.model.Jenkins
import hudson.model.*
import hudson.util.Secret;



String openshiftPodNamespace=new File('/var/run/pod/namespace').getText('UTF-8').trim()
String openshiftSecretName = new File('/var/run/secrets/jenkins-slave-user/metadata.name').getText('UTF-8').trim()
String username = new File('/var/run/secrets/jenkins-slave-user/username').getText('UTF-8').trim()

User u = User.get(username)
def apiToken=u.getProperty(jenkins.security.ApiTokenProperty.class)

//BEFORE 2.129+: https://jenkins.io/blog/2018/07/02/new-api-token-system/
//println "\'${u.getId()}\' API token:${apiToken.getApiTokenInsecure()}"
//['oc','patch', "secret/${openshiftSecretName}", '-p', '{"stringData": {"password": "'+apiToken.getApiTokenInsecure()+'"}}', '-n', openshiftPodNamespace].execute().waitFor()

//AFTER 2.129+: https://jenkins.io/blog/2018/07/02/new-api-token-system/

//Revoke all existing tokens
for (def token:apiToken.getTokenList()){
    def revoked = apiToken.tokenStore.revokeToken(token.uuid)
    if(revoked != null){
        p.tokenStats.removeId(revoked.getUuid());
    }
}
def newToken= apiToken.tokenStore.generateNewToken('swarm')
['oc','patch', "secret/${openshiftSecretName}", '-p', '{"stringData": {"password": "'+newToken.plainValue+'"}}', '-n', openshiftPodNamespace].execute().waitFor()
println "\'${u.getId()}\' API token:${newToken.plainValue}"
u.save()

Jenkins.instance.getAuthorizationStrategy().add(hudson.slaves.SlaveComputer.CREATE, username)
Jenkins.instance.getAuthorizationStrategy().add(hudson.slaves.SlaveComputer.CONNECT, username)
Jenkins.instance.getAuthorizationStrategy().add(Jenkins.READ, username)
u.save();
