## How to contribute

Government employees, the public and members of the private sector are encouraged to contribute.

All contributors retain original copyright, but are granting a world-wide, royalty-free, perpetual, irrevocable, non-exclusive, transferable license to all users.  This project is covered by an [Apache v2.0 license](https://github.com/bcgov/gwells/blob/master/LICENSE).

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

View existing branches.

```
git branch -avv
```

Delete local and remote branches once they have been merged.
```
git branch -d <feature branch>
git push -d origin <feature branch>
```
