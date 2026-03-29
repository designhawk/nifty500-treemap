#!/usr/bin/env python3
"""Build site/data.json by aggregating raw stock data into sector aggregates."""

import csv
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone

BASE_DIR = Path(__file__).parent
RAW_DATA_DIR = BASE_DIR / "raw_data"
STOCKS_CSV = BASE_DIR / "nifty500.csv"
OUTPUT_FILE = BASE_DIR / "docs" / "data.json"


def load_stocks() -> dict[str, dict]:
    stocks = {}
    with open(STOCKS_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stocks[row["symbol"]] = row
    return stocks


def build_sector_data() -> dict:
    raw_files = list(RAW_DATA_DIR.glob("*.json"))
    print(f"Loading {len(raw_files)} raw data files...")

    sector_stocks: dict[str, list] = defaultdict(list)
    skipped = 0

    for f in raw_files:
        try:
            with open(f, encoding="utf-8") as fp:
                data = json.load(fp)
        except Exception:
            skipped += 1
            continue

        if data.get("error"):
            skipped += 1
            continue

        sector = data.get("sector") or "Unknown"
        mcap = data.get("mcap")
        if mcap is None:
            skipped += 1
            continue

        stock_entry = {
            "symbol": data.get("symbol"),
            "name": data.get("company_name", ""),
            "price": data.get("price"),
            "mcap": mcap,
            "returns": data.get("returns", {}),
            "logo_url": data.get("logo_url"),
        }
        sector_stocks[sector].append(stock_entry)

    print(
        f"Skipped {skipped} stocks, kept {sum(len(v) for v in sector_stocks.values())} in {len(sector_stocks)} sectors"
    )

    sectors = []
    for sector, stocks in sector_stocks.items():
        total_mcap = sum(s["mcap"] for s in stocks if s["mcap"])
        n = len(stocks)

        def avg_return(key):
            vals = [s["returns"].get(key) for s in stocks if s["returns"].get(key) is not None]
            return round(sum(vals) / len(vals), 2) if vals else None

        sorted_stocks = sorted(stocks, key=lambda s: s["mcap"] or 0, reverse=True)

        sectors.append(
            {
                "name": sector,
                "total_mcap": total_mcap,
                "stock_count": n,
                "avg_1d": avg_return("1d"),
                "avg_1w": avg_return("1w"),
                "avg_1m": avg_return("1m"),
                "stocks": sorted_stocks,
            }
        )

    sectors.sort(key=lambda s: s["total_mcap"], reverse=True)

    result = {
        "sectors": sectors,
        "meta": {
            "total_sectors": len(sectors),
            "total_stocks": sum(s["stock_count"] for s in sectors),
            "generated": str(Path(__file__).parent / "raw_data"),
            "last_updated": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        },
    }

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nSaved to {OUTPUT_FILE}")
    print(f"Sectors: {len(sectors)}")
    print(f"\nTop 10 sectors by market cap:")
    for s in sectors[:10]:
        print(
            f"  {s['name']}: {s['stock_count']} stocks, 1d={s['avg_1d']}%, 1w={s['avg_1w']}%, 1m={s['avg_1m']}%"
        )

    return result


if __name__ == "__main__":
    build_sector_data()
