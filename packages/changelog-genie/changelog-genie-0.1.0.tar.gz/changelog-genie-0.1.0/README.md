# Changelog Genie

![](changelog-genie.png)

Image Credit: DALL-E

## Overview

Changelog Genie is a simple and pragmatic changelog generator, implemented in Python, that utilizes both the Git CLI 
and the GitHub REST API to produce changelog content very efficiently, avoiding GitHub API rate limits. It was built 
out of necessity as a replacement for [github-changelog-generator](https://github.com/github-changelog-generator/github-changelog-generator),
which served well for many Apache Arrow projects for a long time but eventually became unworkable as the number of 
issues and pull requests continued to grow.

Roadmap/Status:

- [x] Basic functionality in place
- [ ] Make sections and labels configurable
- [ ] Support reading [github-changelog-generator](https://github.com/github-changelog-generator/github-changelog-generator) configuration files
- [ ] Write the content into an existing changelog file

## Usage

There is currently a three-step process for generating a changelog. This will be improved in a future release.

### Step 1: Generate a list of commit hashes

From the working directory of the project that contains commits to be documented, run a `git log` command to generate 
a list of commit hashes to be documented. For example, to list commits between two tagged 
releases `0.1.0` and `0.2.0`: 

```shell
git log 0.1.0..0.2.0 --pretty=format:"%H" > commits.txt
```

### Step 2: Generate changelog contents for this release

Run the ChangeLog Genie script to fetch the commits from GitHub and produce the changelog content. Providing a GitHub token is 
necessary to achieve a higher rate limit for interaction with the GitHub REST API. 

```shell
GITHUB_TOKEN=<token> python3 changelog_genie.py apache/arrow-datafusion path/to/commits.txt > partial-changelog.md
```

### Step 3: Copy and paste into existing changelog

This will be automated in a future release.

## Contributing

```shell
python3 -m venv venv
# activate the venv
source venv/bin/activate
# update pip itself if necessary
python -m pip install -U pip
# install dependencies (for Python 3.8+)
python -m pip install -r requirements.in

Poetry

```shell
sudo apt install python3-poetry
```

Testing

```shell
poetry build
python -m pip install -e .
```

