## How to contribute

Government employees, public and members of the private sector are encouraged to contribute to the repository by **forking and submitting a pull request**.

(If you are new to GitHub, you might start with a [basic tutorial](https://help.github.com/articles/set-up-git) and check out a more detailed [guide to pull requests](https://help.github.com/articles/using-pull-requests/).)

Pull requests will be evaluated by the repository guardians on a schedule and if deemed beneficial will be committed to the master.

All contributors retain the original copyright to their stuff, but by contributing to this project, you grant a world-wide, royalty-free, perpetual, irrevocable, non-exclusive, transferable license to all users **under the terms of the [license](https://github.com/bcgov/gwells/blob/master/LICENSE) under which this project is distributed**.

#### Prerequisites

Fork our repository.

* Create a [GitHub account](https://github.com/join)
* Visit our [repository](https://github.com/bcgov/gwells)
* Create your [own fork](https://github.com/bcgov/gwells/fork)

Optional: Set nano as default command line editor.

```
git config --global core.editor "nano"
```

#### Clone, Branch and Push

Clone and navigate into your repository.

```
git clone https://github.com/<github name>/gwells
cd gwells
```

Create a feature branch with a meaningful name and push it to your repo.  Pick a name that describes the feature.

```
git checkout -b <feature branch>
git push --set-upstream origin <feature branch>
```

Add and push files as required.

```
git add <this file or path>
git commit -m "<meaningful message>"
git push
```

#### Upstream Updates


GWells uses a master and a release branch, which is replaced regularly.

* master
* release -> ```release/1.<sprint number>.<hotfix number>```

Set that repository as your upstream remote and verify.

```
git remote add upstream https://github.com/bcgov/gwells
git remote -v
```

Pull from the upstream release branch at least daily.

```
git merge upstream/release/1.32.0 --no-commit
```

When ready create a pull request into the release branch.

#### Continuous Integration and Continuous Deployment

We use continuous integration to test, build and accept code into the release branch.  We use continuous integration and continuous deployment to get that code from the release branch into master branch eventually deployed into [production]().

Pull requests trigger a Jenkins pipeline.  View the status of any [existing pull requests](https://github.com/bcgov/gwells/pulls) from the link below.

https://github.com/bcgov/gwells/pulls

Verify that all tests have passed.  If you have access to Jenkins, then accept that pull request when successful.  If not, then please wait to hear from someone in the GWells team.

Please be aware that no code can be accepted without receiving at least one review from a GWells team member.

#### Cleanup

We recommend that feature branches be deleted after acceptance into our release branch.

View existing branches.

```
git branch -avv
```

Delete local branches.  May not be the default or current branch.
```
git branch -d <feature branch>
```

Delete stale remote branches.

```
git push -d origin <feature branch>
```

Update remote and local branches.  Local, unpushed branches must be cleaned up manually.

```
git remote update origin --prune
git remote update upstream --prune
```
