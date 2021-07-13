#!/usr/bin/env groovy

//
// This needs to come before 003-register-github-webhooks.groovy
//

import static jenkins.model.Jenkins.instance as jenkins

import com.cloudbees.hudson.plugins.folder.computed.DefaultOrphanedItemStrategy
import org.jenkinsci.plugins.github_branch_source.*
import jenkins.scm.impl.trait.*
import jenkins.scm.api.mixin.*
import org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject
import jenkins.branch.BranchSource

import com.adobe.jenkins.disable_github_multibranch_status.DisableStatusUpdateTrait
import jenkins.plugins.git.traits.WipeWorkspaceTrait
import org.csanchez.jenkins.plugins.kubernetes.KubernetesFolderProperty

// Get configuration from jobs configmap
def repoOwner = new File('/var/run/configs/jobs/repo.owner').getText('UTF-8').trim()
def appRepoAdmin = new File('/var/run/configs/jobs/repo.name.Admin').getText('UTF-8').trim()
def appRepoApi = new File('/var/run/configs/jobs/repo.name.Api').getText('UTF-8').trim()
def appRepoPublic = new File('/var/run/configs/jobs/repo.name.Public').getText('UTF-8').trim()
def appName = new File('/var/run/configs/jobs/app.name').getText('UTF-8').trim()
def name = appName.toLowerCase().replaceAll("/[^A-Za-z0-9 ]/", "").replaceAll("\\s", "-")

def githubCredentialsId = "github-account"

def pullRequestTraits = [
    new ForkPullRequestDiscoveryTrait([ChangeRequestCheckoutStrategy.MERGE].toSet(),new ForkPullRequestDiscoveryTrait.TrustContributors()),
    new DisableStatusUpdateTrait(),
    new WipeWorkspaceTrait()
]

def masterTraits = [
    new RegexSCMHeadFilterTrait("^(develop|test|master)"),
    new BranchDiscoveryTrait(3),
    new DisableStatusUpdateTrait(),
    new WipeWorkspaceTrait()
]

def hotfixTraits = [
    new RegexSCMHeadFilterTrait("^(hotfix)"),
    new BranchDiscoveryTrait(3),
    new DisableStatusUpdateTrait(),
    new WipeWorkspaceTrait()
]

core_jobs = [ new Expando(jobName: "dev-${name}-public",
                          displayName: "dev-${name}-public",
                          owner: repoOwner,
                          repo: appRepoPublic,
                          credentialsId: githubCredentialsId,
                          jenkinsFilePath: "Jenkinsfile-develop",
                          traits: pullRequestTraits,
                          startJob: true),
                   new Expando(jobName: "dev-${name}-api",
                          displayName: "dev-${name}-api",
                          owner: repoOwner,
                          repo: appRepoApi,
                          credentialsId: githubCredentialsId,
                          jenkinsFilePath: "Jenkinsfile-develop",
                          traits: pullRequestTraits,
                          startJob: true),
                   new Expando(jobName: "dev-${name}-admin",
                          displayName: "dev-${name}-admin",
                          owner: repoOwner,
                          repo: appRepoAdmin,
                          credentialsId: githubCredentialsId,
                          jenkinsFilePath: "Jenkinsfile-develop",
                          traits: pullRequestTraits,
                          startJob: true),
                    new Expando(jobName: "cicd-${name}-public",
                          displayName: "cicd-${name}-public",
                          owner: repoOwner,
                          repo: appRepoPublic,
                          credentialsId: githubCredentialsId,
                          jenkinsFilePath: "Jenkinsfile-cicd",
                          traits: masterTraits,
                          startJob: true),
                   new Expando(jobName: "cicd-${name}-api",
                          displayName: "cicd-${name}-api",
                          owner: repoOwner,
                          repo: appRepoApi,
                          credentialsId: githubCredentialsId,
                          jenkinsFilePath: "Jenkinsfile-cicd",
                          traits: masterTraits,
                          startJob: true),
                   new Expando(jobName: "cicd-${name}-admin",
                          displayName: "cicd-${name}-admin",
                          owner: repoOwner,
                          repo: appRepoAdmin,
                          credentialsId: githubCredentialsId,
                          jenkinsFilePath: "Jenkinsfile-cicd",
                          traits: masterTraits,
                          startJob: true),
                    new Expando(jobName: "hotfix-${name}-public",
                          displayName: "hotfix-${name}-public",
                          owner: repoOwner,
                          repo: appRepoPublic,
                          credentialsId: githubCredentialsId,
                          jenkinsFilePath: "Jenkinsfile-hotfix",
                          traits: hotfixTraits,
                          startJob: true),
                   new Expando(jobName: "hotfix-${name}-api",
                          displayName: "hotfix-${name}-api",
                          owner: repoOwner,
                          repo: appRepoApi,
                          credentialsId: githubCredentialsId,
                          jenkinsFilePath: "Jenkinsfile-hotfix",
                          traits: hotfixTraits,
                          startJob: true),
                   new Expando(jobName: "hotfix-${name}-admin",
                          displayName: "hotfix-${name}-admin",
                          owner: repoOwner,
                          repo: appRepoAdmin,
                          credentialsId: githubCredentialsId,
                          jenkinsFilePath: "Jenkinsfile-hotfix",
                          traits: hotfixTraits,
                          startJob: true),
            ]


jobs = jenkins.getAllItems()

for (core_job in core_jobs) {

  def shouldCreate = true
  jobs.each { j ->
      if (j instanceof org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject &&
          j.fullName.contains(core_job.jobName)) {
          println '----> Already have a job for ' + j.fullName + ' of type:' + j.getClass()
          println j
          shouldCreate = false
      }
  }
  if (!shouldCreate) {
      continue
  }
  println '----> configuring job ' + core_job.jobName

  // start by creating the toplevel folder
  def folder = jenkins.createProject(WorkflowMultiBranchProject, core_job.jobName)

  // Configure the Github SCM integration
  def scm = new GitHubSCMSource(core_job.owner, core_job.repo)
  scm.credentialsId = core_job.credentialsId
  scm.traits = core_job.traits
  folder.getSourcesList().add(new BranchSource(scm))

  folder.displayName = core_job.displayName

  // Delete orphan items after 5 days
  folder.orphanedItemStrategy = new DefaultOrphanedItemStrategy(true, "-1", "-1")

  // Configure what Jenkinsfile we should be looking for
  folder.projectFactory.scriptPath = core_job.jenkinsFilePath

  folder.addProperty(new KubernetesFolderProperty())

  folder.triggers.clear()

  jenkins.save()

  println '----> configured job ' + core_job.jobName

  if (core_job.startJob) {
    Thread.start {
        sleep 3000 // 3 seconds
        println '----> Running Github organization scan for job ' + core_job.jobName
        folder.scheduleBuild()
    }
  }
}


println '<--- Create Jobs: jobs created.'