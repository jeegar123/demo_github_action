from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    output_dir = Path("generated")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    file_path = output_dir / f"file-{timestamp}.txt"
    file_path.write_text(
        f"This file was created by GitHub Actions at {timestamp} UTC.\n",
        encoding="utf-8",
    )
    print(f"Created: {file_path}")


if __name__ == "__main__":
    main()
