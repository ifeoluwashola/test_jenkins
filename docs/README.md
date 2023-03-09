# IE GitHub Template Standards and Best Practices Documentation

This README.md file documents standards and best practices for implementing GitHub repositories for Innovation Edge projects.

All standards and best practices documentation should be captured and/or linked to from this README.md file in the sections below.

For more recommendations and best practices, we recommend checking out the [AIDE User Guide](https://wwwin-github.cisco.com/pages/AIDE/User-Guide/stable/recommendations/github.html).

## README

The README.md file at the root of your GitHub repository should provide a "launch pad" for accessing all required documentation and resources for your project.  The standard format of this file to which your repository should adhere is captured in our [README.md](../README.md) template.  

## CHANGELOG

A CHANGELOG.md is a file that shares a chronologically ordered list of the changes you’ve made on your project. A changelog is a kind of summary of added, changed, fixed, deprecated, and removed features. It should be easy to understand both by the users using your project and the developers working on it.  You can use the [CHANGELOG.md](../CHANGELOG.md) file of this project as a template.  Any notable implemented via PRs should be added to CHANGELOG.md as part of the PR process and caputed under the `Unreleased` section so that it can eventually be moved to the proper version section once a release is ready to be delivered.  For more information, see https://keepachangelog.com.

## Roadmap Wiki

We use the Wiki feature of GitHub to for capturing product roadmap plans.  See [this project's wiki](https://wwwin-github.cisco.com/spa-ie/ie-github-template/wiki) for an example of what this should look like.  The Roadmap Wiki is typically where new feature tracking will begin for a project.  At some point, the full requirements documentation for a new feature should be captured as a [GitHub Issue](https://wwwin-github.cisco.com/spa-ie/ie-github-template/issues) on your GitHub repo, and then tracked in [Rally](rally1.rallydev.com/) as a new Feature with associated User Stories for tracking in IE team sprints.


## GitHub Flow and Branching

[GitHub flow](https://githubflow.github.io/) is a lightweight, branch-based workflow that supports teams and projects where deployments are made regularly.  The GitHub flow process should be followed whenever making changes to code.  We typically will follow a simple approach, with a single `main` branch, and individual branches for and changes (e.g. new features or fixes) that need to be committed.  A Pull Request for your branch should be submitted whenever code needs to be merged to the `main` branch, and at least one reviewer should approve your changes before merging.

The IE team's own version of GitHub flow should work roughly as follows when developing a new Feature:

1. Document your new feature in the GitHub Wiki Roadmap page.
2. Create a GitHub Issue to track the requirements for your feature.
3. Add a Feature to Rally and a link to the GitHub Issues in the Rally Feature description. 
4. When we are ready to work on a Feature, schedule requirements discussions as needed with stakeholders, create corresponding User Stories in Rally under your Feature, and assign to the User Stories to a Sprint/Iteration as appropriate
5. When you're ready to start writing code, create your feature branch in Github
6. Write your code and commit changes to your branch
7. Open a Pull Request and assign reviewers to initiate discussion about your commits
8. Discuss and review your code (and make any necessary changes)
9. When PR is reviewed and approved, merge to main and delete your branch
10. Update the state of User Stories and Feature in Rally to reflect your changes

### Branch Naming

Branches should be named as follows, capturing both the associated GitHub Issue # and a brief description of the feature/fix being developed.

Example: `0016_add-support-for-x`

In the above example, 0016 refers to Issue #16, and the description of the change described by Issue #16 is "Add Support for X".

## Repository Settings

### Branching Protection Rules

Under **Settings > Branches**, a Branch Protection Rule should be applied to the `main` branch with the following settings:

- *Branch name pattern:* main
- *Require pull request reviews before merging*

This ensures that unless the code contributor is an admin on the project, they must follow the GitHub Flow standard procedure which includes a peer review and approval of their code changes via a Pull Request.

## Template Files

Located in the [.github](../.github) folder.

### PULL_REQUEST_TEMPLATE

[PULL_REQUEST_TEMPLATE.md](../.github/PULL_REQUEST_TEMPLATE.md)

*Documentation to be added*

### ISSUE_TEMPLATE

[ISSUE_TEMPLATE](../.github/ISSUE_TEMPLATE/)

*Documentation to be added*

### CODE_OF_CONDUCT

[CODE_OF_CONDUCT.md](../.github/CODE_OF_CONDUCT.md)

*Documentation to be added*

### CONTRIBUTING

[CONTRIBUTING.rst](../.github/CONTRIBUTING.rst)

*Documentation to be added*

## .gitignore

[.gitignore](../.gitignore)

*Documentation to be added*

## LICENSE

[LICENSE.md](../LICENSE)

*Documentation to be added*
