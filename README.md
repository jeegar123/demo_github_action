# GitHub Action: create a file on a schedule

This repository contains a simple Python script and a GitHub Actions workflow.

## What it does

- Runs on a schedule (`*/5 * * * *`) and can also be started manually.
- Executes `scripts/create_file.py`.
- Creates a timestamped file in `generated/`.
- Commits and pushes the new file back to the repository.

## Important GitHub Actions limits

- GitHub-hosted scheduled workflows cannot reliably run every minute; the practical minimum is every 5 minutes.
- The `schedule` trigger only runs from the repository's **default branch**.

If you need true every-minute execution, use an external scheduler (or a self-hosted runner + cron) to call `workflow_dispatch` or run the script directly.
