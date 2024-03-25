import jenkins.model.Jenkins

import com.cloudbees.plugins.credentials.*;
import com.cloudbees.plugins.credentials.impl.*;
import com.cloudbees.plugins.credentials.domains.*;
import org.jenkinsci.plugins.plaincredentials.impl.*;

import hudson.util.Secret;
import com.cloudbees.jenkins.GitHubWebHook;
import com.cloudbees.jenkins.*
import org.kohsuke.github.*

if (new File('/var/run/secrets/bitbucket/username').exists()){
  String githubUsername = new File('/var/run/secrets/bitbucket/username').getText('UTF-8').trim()
  String githubPassword = new File('/var/run/secrets/bitbucket/password').getText('UTF-8').trim()

  Credentials c1 = (Credentials) new UsernamePasswordCredentialsImpl(
    CredentialsScope.GLOBAL,
    "bitbucket-account",
    "BitBucket account",
    githubUsername,
    githubPassword);

  SystemCredentialsProvider.getInstance().getStore().addCredentials(Domain.global(), c1);


  println "Configuring BitBucket API"
  def bitbucketServerUrl = new File('/var/run/secrets/bitbucket/url').getText('UTF-8').trim()
  def bitbucketConfig = Jenkins.getInstance().getDescriptor(com.cloudbees.jenkins.plugins.bitbucket.endpoints.BitbucketEndpointConfiguration);
  bitbucketConfig.setEndpoints([new com.cloudbees.jenkins.plugins.bitbucket.endpoints.BitbucketServerEndpoint('BitBucket', bitbucketServerUrl, false, 'bitbucket-account')])
}