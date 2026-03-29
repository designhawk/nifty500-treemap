#!/usr/bin/env python3
"""Fetch Nifty 500 constituent list with sectors from NSE India."""

import csv
import time
import requests
from pathlib import Path

NIFTY500_URL = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/",
}

OUTPUT_PATH = Path(__file__).parent.parent / "nifty500.csv"


def fetch_nifty500() -> list[dict]:
    session = requests.Session()
    session.get("https://www.nseindia.com/", headers=HEADERS, timeout=10)
    time.sleep(0.5)
    resp = session.get(NIFTY500_URL, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return data.get("data", [])


def main():
    print("Fetching Nifty 500 constituents...")
    stocks = fetch_nifty500()
    print(f"Got {len(stocks)} stocks")

    rows = []
    for s in stocks:
        symbol = s.get("symbol", "")
        # Skip the index entry itself (first item is "NIFTY 500" index)
        if not symbol or symbol == "NIFTY 500":
            continue
        meta = s.get("meta", {})
        rows.append(
            {
                "symbol": symbol,
                "company_name": meta.get("companyName", ""),
                "sector": meta.get("industry", "") or "Unknown",
                "series": meta.get("series", "") or s.get("series", ""),
            }
        )

    rows.sort(key=lambda x: x["symbol"])

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["symbol", "company_name", "sector", "series"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved to {OUTPUT_PATH}")

    sector_counts: dict[str, int] = {}
    for r in rows:
        sector = r["sector"] or "Unknown"
        sector_counts[sector] = sector_counts.get(sector, 0) + 1

    print(f"\nSectors: {len(sector_counts)}")
    for sector, count in sorted(sector_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {sector}: {count} stocks")


if __name__ == "__main__":
    main()
