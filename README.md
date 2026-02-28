# GitHub Action: create a file every minute

This repository contains a simple Python script and a GitHub Actions workflow.

## What it does

- Runs every minute (`* * * * *`) and can also be started manually.
- Executes `scripts/create_file.py`.
- Creates a timestamped file in `generated/`.
- Commits and pushes the new file back to the repository.

> Note: GitHub's scheduler is not guaranteed to run exactly every minute under all conditions, but this is the closest schedule supported.
