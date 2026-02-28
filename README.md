# GitHub Action: create a file every minute

This repository contains a simple Python script and a GitHub Actions workflow.

## What it does

- Runs automatically every minute (`* * * * *`) and can also be started manually.
- Executes `scripts/create_file.py`.
- Creates a timestamped file in `generated/`.
- Commits and pushes the new file back to the repository.

## If it is not running automatically

Check these required conditions in GitHub:

1. The workflow file is on the repository **default branch**.
2. **Actions are enabled** for the repository.
3. The workflow is not disabled (in Actions tab, click **Enable workflow** if needed).
4. There has been recent repository activity (scheduled workflows may be delayed by GitHub).

> Note: GitHub may occasionally delay or skip a minute-level scheduled run under load, but this workflow is configured for every minute.
