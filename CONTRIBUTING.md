## How to contribute

Government employees, public and members of the private sector are encouraged to contribute to the repository by **forking and submitting a pull request**.

(If you are new to GitHub, you might start with a [basic tutorial](https://help.github.com/articles/set-up-git) and check out a more detailed [guide to pull requests](https://help.github.com/articles/using-pull-requests/).)

Pull requests will be evaluated by the repository guardians on a schedule and if deemed beneficial will be committed to the master.

All contributors retain the original copyright to their stuff, but by contributing to this project, you grant a world-wide, royalty-free, perpetual, irrevocable, non-exclusive, transferable license to all users **under the terms of the [license](https://github.com/bcgov/gwells/blob/master/LICENSE) under which this project is distributed**.

---

### Prerequisites

* [GitHub account](https://github.com/join)
* [Your own fork](https://github.com/bcgov/gwells/fork)

### Clone, Branch and Push

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

### Upstream Updates

Set the upstream repository.

```
git remote add upstream https://github.com/bcgov/gwells
```

Pull from and send pull requests to the temporary release branch.

```
git pull upstream/<release branch> --rebase
git push origin -f
```

* release branch = ```release/<major release>.<sprint number>.<hotfix number>```

### Continuous Integration and Continuous Deployment

We use a Jenkins pipleline to test, build and integrate pull requests into temporary release branches.  Those branches are merged into master and deployed into production approximately every two weeks, coinciding with the end of an agile sprint.

GWells members are responsible for integrating their own code in through Jenkins.  Outside collaborators, please submit pull requests and watch the build and tests statuses.  All pull requests require a review.

### Cleanup

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

Prune remote and local branches.  Local, unpushed branches must be cleaned up manually.

```
git remote update origin --prune
git remote update upstream --prune
```
