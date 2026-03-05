# GitHub Action: create a file on a schedule

This repository contains a simple Python script and a GitHub Actions workflow.

## What it does

- Runs on a schedule (`*/5 * * * *`) and can also be started manually.
- Executes `scripts/create_file.py`.
- Creates a timestamped file in `generated/`.
- Commits and pushes the new file back to the repository.

## Google Shopping scraper script

You can also run a CLI scraper that fetches Google Shopping results for a product name:

```bash
python3 scripts/scrape_google_shopping.py "iphone 15" --limit 5
```

Save output to a file:

```bash
python3 scripts/scrape_google_shopping.py "nike shoes" --limit 10 --output output/products.json
python3 scripts/scrape_google_shopping.py "nike shoes" --limit 10 --output output/products.csv
```

### Notes

- This scraper uses Google web pages directly, which can be rate limited or blocked.
- If Google serves a CAPTCHA or changes HTML structure, extraction may fail.
- No third-party packages are required (Python standard library only).

## Important GitHub Actions limits

- GitHub-hosted scheduled workflows cannot reliably run every minute; the practical minimum is every 5 minutes.
- The `schedule` trigger only runs from the repository's **default branch**.

If you need true every-minute execution, use an external scheduler (or a self-hosted runner + cron) to call `workflow_dispatch` or run the script directly.
