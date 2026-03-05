# GitHub Action examples: file generation + Discord app heartbeat

This repository contains two simple Python + GitHub Actions examples.

## 1) Create a file on a schedule

- Runs on a schedule (`*/5 * * * *`) and can also be started manually.
- Executes `scripts/create_file.py`.
- Creates a timestamped file in `generated/`.
- Commits and pushes the new file back to the repository.

Workflow: `.github/workflows/create-file-every-minute.yml`

## 2) Discord app heartbeat from GitHub Actions

- Runs on a schedule (`*/5 * * * *`) and can also be started manually.
- Executes `scripts/discord_app.py`.
- Sends a heartbeat message to Discord using a webhook URL stored in GitHub Secrets.

Workflow: `.github/workflows/discord-app-heartbeat.yml`

### Setup steps

1. In Discord, create a server webhook and copy its URL.
2. In GitHub, open **Settings → Secrets and variables → Actions**.
3. Add a new repository secret named `DISCORD_WEBHOOK_URL`.
4. Run the **Discord app heartbeat** workflow manually once via `workflow_dispatch` to verify.

## Important GitHub Actions limits

- GitHub-hosted scheduled workflows cannot reliably run every minute; the practical minimum is every 5 minutes.
- The `schedule` trigger only runs from the repository's **default branch**.

If you need true every-minute execution, use an external scheduler (or a self-hosted runner + cron) to call `workflow_dispatch` or run the script directly.
