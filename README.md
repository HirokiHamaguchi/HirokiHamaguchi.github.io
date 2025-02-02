# HirokiHamaguchi.github.io

This is my personal website.

[https://hirokihamaguchi.github.io/](https://hirokihamaguchi.github.io/)

This repository uses the template of [Academic Pages](https://github.com/academicpages/academicpages.github.io)

## How to Run Locally

```bash
sudo apt install ruby-dev ruby-bundler nodejs
bundle install
jekyll serve -l -H localhost
```

## How to Update with the Upstream

```bash
git remove -v # Check the upstream exists
git fetch upstream # Fetch the upstream
git log upstream/master --oneline # Check the upstream log
git checkout master # If you are already in the master branch, skip this
git rebase --onto master xxxxxx upstream/master # xxxxxx is the commit hash of the last commit before the unmerged commit
# Fix the conflict if any
git checkout master # Turn back to the master branch
git merge @{-1} # Merge the rebased branch
```

## LICENSE

We use the MIT License. Please see the [LICENSE](LICENSE) file for details.
