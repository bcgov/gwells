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
