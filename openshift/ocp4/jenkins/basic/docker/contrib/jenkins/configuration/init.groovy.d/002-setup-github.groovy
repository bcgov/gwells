import jenkins.model.Jenkins

import com.cloudbees.plugins.credentials.*;
import com.cloudbees.plugins.credentials.impl.*;
import com.cloudbees.plugins.credentials.domains.*;
import org.jenkinsci.plugins.plaincredentials.impl.*;

import hudson.util.Secret;
import com.cloudbees.jenkins.GitHubWebHook;
import com.cloudbees.jenkins.*
import org.kohsuke.github.*

if (new File('/var/run/secrets/github/username').exists()){
  String githubUsername = new File('/var/run/secrets/github/username').getText('UTF-8').trim()
  String githubPassword = new File('/var/run/secrets/github/password').getText('UTF-8').trim()

  Credentials c1 = (Credentials) new UsernamePasswordCredentialsImpl(
    CredentialsScope.GLOBAL,
    "github-account",
    "GitHub account",
    githubUsername,
    githubPassword);

  SystemCredentialsProvider.getInstance().getStore().addCredentials(Domain.global(), c1);

  Credentials c2 = (Credentials) new StringCredentialsImpl(
    CredentialsScope.GLOBAL,
    "github-access-token",
    "GitHub account (Access Token)",
    Secret.fromString(githubPassword));

  SystemCredentialsProvider.getInstance().getStore().addCredentials(Domain.global(), c2);

  println "Configuring GitHub API"

  def ghCofigs = Jenkins.getInstance().getDescriptor(org.jenkinsci.plugins.github.config.GitHubPluginConfig.class).getConfigs();
  def ghServerConfig = new org.jenkinsci.plugins.github.config.GitHubServerConfig('github-access-token');
  ghServerConfig.setName('GitHub')
  ghServerConfig.setApiUrl('https://api.github.com')
  ghServerConfig.setManageHooks(true);
  ghServerConfig.setClientCacheSize(21)
  ghCofigs.clear();
  ghCofigs.add(ghServerConfig);
}