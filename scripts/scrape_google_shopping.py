#!/usr/bin/env python3
"""Scrape product listings from Google Shopping search results."""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

GOOGLE_SHOPPING_URL = "https://www.google.com/search?tbm=shop&q={query}"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/123.0.0.0 Safari/537.36"
)


@dataclass
class Product:
    title: str
    price: str
    merchant: str
    url: str


def build_search_url(query: str) -> str:
    return GOOGLE_SHOPPING_URL.format(query=quote_plus(query))


def get_html(search_url: str, timeout: float = 20.0) -> str:
    request = Request(
        search_url,
        headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"},
    )
    with urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8", errors="ignore")

    if "Our systems have detected unusual traffic" in body:
        raise RuntimeError(
            "Google blocked this request (likely CAPTCHA/anti-bot). Try again later."
        )
    return body


def clean_text(text: str) -> str:
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", text)).split())


def extract_first(patterns: Iterable[str], text: str) -> str:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I | re.S)
        if match:
            return clean_text(match.group(1))
    return ""


def parse_products(html_doc: str, limit: int = 10) -> list[Product]:
    card_patterns = [
        r'(<div[^>]+class="[^"]*sh-dgr__grid-result[^"]*"[\s\S]*?</div>\s*</div>)',
        r'(<div[^>]+class="[^"]*sh-dlr__list-result[^"]*"[\s\S]*?</div>\s*</div>)',
    ]

    cards: list[str] = []
    for pattern in card_patterns:
        cards = re.findall(pattern, html_doc, flags=re.I)
        if cards:
            break

    if not cards:
        # Fallback: search in chunks around product link markers.
        for marker in re.finditer(r"/shopping/product/", html_doc):
            start = max(0, marker.start() - 2000)
            end = min(len(html_doc), marker.end() + 3000)
            cards.append(html_doc[start:end])

    products: list[Product] = []
    seen_titles: set[str] = set()
    for card in cards:
        title = extract_first(
            [
                r"<h3[^>]*>(.*?)</h3>",
                r'class="[^"]*tAxDx[^"]*"[^>]*>(.*?)</',
                r'class="[^"]*Xjkr3b[^"]*"[^>]*>(.*?)</',
            ],
            card,
        )
        price = extract_first(
            [
                r'class="[^"]*a8Pemb[^"]*"[^>]*>(.*?)</',
                r'class="[^"]*kHxwFf[^"]*"[^>]*>(.*?)</',
                r"([$€£]\s?\d[\d,]*(?:\.\d{1,2})?)",
            ],
            card,
        )
        merchant = extract_first(
            [
                r'class="[^"]*aULzUe[^"]*"[^>]*>(.*?)</',
                r'class="[^"]*IuHnof[^"]*"[^>]*>(.*?)</',
            ],
            card,
        )
        url = ""
        url_match = re.search(r'href="([^"]*(?:/shopping/product/|/url\?q=)[^"]*)"', card)
        if url_match:
            url = html.unescape(url_match.group(1))
            if url.startswith("/"):
                url = f"https://www.google.com{url}"

        if not title or title in seen_titles:
            continue

        seen_titles.add(title)
        products.append(Product(title=title, price=price, merchant=merchant, url=url))
        if len(products) >= limit:
            break

    return products


def save_as_csv(products: list[Product], output_path: Path) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "merchant", "url"])
        writer.writeheader()
        for product in products:
            writer.writerow(asdict(product))


def save_as_json(products: list[Product], output_path: Path) -> None:
    payload = [asdict(product) for product in products]
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape Google Shopping search results for a product name."
    )
    parser.add_argument("query", help="Product name to search for, e.g. 'iphone 15'.")
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of products to return (default: 10).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output path. Use .json or .csv extension.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.limit < 1:
        print("--limit must be at least 1", file=sys.stderr)
        return 2

    search_url = build_search_url(args.query)
    try:
        page_html = get_html(search_url)
        products = parse_products(page_html, limit=args.limit)
    except (HTTPError, URLError) as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        return 1
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if not products:
        print(
            "No products extracted. Google may have changed markup or blocked the request.",
            file=sys.stderr,
        )
        return 1

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        suffix = args.output.suffix.lower()
        if suffix == ".csv":
            save_as_csv(products, args.output)
        else:
            save_as_json(products, args.output)
        print(f"Saved {len(products)} products to {args.output}")
    else:
        print(json.dumps([asdict(p) for p in products], ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
