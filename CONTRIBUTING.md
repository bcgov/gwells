## How to contribute

Government employees, the public and members of the private sector are encouraged to contribute.

All contributors retain original copyright, but are granting a world-wide, royalty-free, perpetual, irrevocable, non-exclusive, transferable license to all users.  This project is covered by an [Apache v2.0 license](https://github.com/bcgov/gwells/blob/master/LICENSE).

### Prerequisites

* [GitHub account](https://github.com/join)
* [Your own fork](https://github.com/bcgov/gwells/fork)

### Assumptions

For convenience this guide will use the following:

* GitHub username = stinkypete
* Current release = 1.32.0
* Feature branch = myFeature

### Clone, Branch and Push

Clone and navigate into your repository.

```
git clone https://github.com/stinkypete/gwells
cd gwells
```

Create a feature branch with a meaningful name and push it to your repo.  Pick a name that describes the feature.

```
git checkout -b myFeature
git push --set-upstream origin myFeature
```

Add and push files as required.

```
git add CONTRIBUTING.md
git commit -m "This line was copied and pasted from CONTRIBUTING.md!"
git push
```

### Upstream Updates

Set the upstream repository.

```
git remote add upstream https://github.com/bcgov/gwells
```

Pull from the current release branch at least daily.

```
git pull upstream release/1.32.0 --rebase
git push origin -f
```

* release branch = ```release/<major release>.<sprint number>.<hotfix number>```

### Pull Requests

When a feature is ready for testing please send a pull request to our current release branch.

When a pull request is related to a [GWELLS Trello board](https://trello.com/b/2UQZgXHR/wells-project-board) product backlog, your pull request title must match the following naming convention:
> [Trello CardId] Trello Title 

E.g.
> [405] Bug to be fixed

Find the Trello cardId in the card url.

### Continuous Integration and Continuous Deployment

We use a Jenkins pipleline to test, build and integrate pull requests into release branches.  Those branches are merged into master and deployed into production approximately every two weeks, coinciding with the end of an agile sprint.

GWells members are responsible for integrating their own code in through Jenkins.  Outside collaborators, please submit pull requests and watch the build and tests statuses.  All pull requests require a review.

### Cleanup

View existing branches.

```
git branch -avv
```

Delete local and remote branches once they have been merged.
```
git branch -d myFeature
git push -d origin myFeature
```
