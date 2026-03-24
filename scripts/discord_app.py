from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def build_message() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    return f"🤖 Discord app heartbeat from GitHub Actions at {timestamp}"


def send_webhook(webhook_url: str, content: str) -> None:
    payload = json.dumps({"content": content}).encode("utf-8")
    request = Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=15) as response:
        status_code = response.getcode()
        if not (200 <= status_code < 300):
            raise RuntimeError(f"Discord webhook failed with status: {status_code}")


def main() -> int:
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("Missing required environment variable: DISCORD_WEBHOOK_URL", file=sys.stderr)
        return 1

    message = build_message()

    try:
        send_webhook(webhook_url, message)
    except (HTTPError, URLError, RuntimeError) as error:
        print(f"Failed to send Discord message: {error}", file=sys.stderr)
        return 1

    print("Discord webhook message sent successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
