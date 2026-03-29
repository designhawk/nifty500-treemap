#!/usr/bin/env python3
"""Fetch yfinance data for all Nifty 500 stocks and save to raw_data/."""

import csv
import json
import time
import random
from pathlib import Path

import yfinance as yf

BASE_DIR = Path(__file__).parent
STOCKS_CSV = BASE_DIR / "nifty500.csv"
RAW_DATA_DIR = BASE_DIR / "raw_data"
DOMAIN_MAP_FILE = BASE_DIR / "domain_map.json"

with open(DOMAIN_MAP_FILE, "r") as f:
    DOMAIN_MAP = json.load(f)


def fetch_logo_url(symbol: str) -> str | None:
    domain = DOMAIN_MAP.get(symbol)
    if domain:
        return f"https://cdn.tickerlogos.com/{domain}"
    return None


def load_stocks() -> list[dict]:
    with open(STOCKS_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def fetch_stock(symbol: str) -> dict | None:
    ticker = yf.Ticker(f"{symbol}.NS")
    try:
        info = ticker.fast_info
    except Exception:
        return None

    try:
        hist = ticker.history(period="1mo", auto_adjust=True)
    except Exception:
        hist = None

    mcap = getattr(info, "market_cap", None) or getattr(info, "valuation", None)
    price = getattr(info, "last_price", None)

    returns = {"1d": None, "1w": None, "1m": None}
    if hist is not None and len(hist) >= 2:
        prices = hist["Close"].dropna()
        if len(prices) >= 2:
            current = prices.iloc[-1]
            week_ago = prices.iloc[-6] if len(prices) >= 6 else prices.iloc[0]
            month_ago = prices.iloc[-22] if len(prices) >= 22 else prices.iloc[0]
            day_ago = prices.iloc[-2] if len(prices) >= 2 else current

            returns["1d"] = round((current - day_ago) / day_ago * 100, 2) if day_ago else None
            returns["1w"] = round((current - week_ago) / week_ago * 100, 2) if week_ago else None
            returns["1m"] = round((current - month_ago) / month_ago * 100, 2) if month_ago else None

    logo_url = fetch_logo_url(symbol)

    return {
        "symbol": symbol,
        "price": round(price, 2) if price else None,
        "mcap": mcap,
        "returns": returns,
        "logo_url": logo_url,
    }


def main():
    RAW_DATA_DIR.mkdir(exist_ok=True)
    stocks = load_stocks()
    print(f"Loaded {len(stocks)} stocks from {STOCKS_CSV}")

    for i, stock in enumerate(stocks):
        symbol = stock["symbol"]
        out_file = RAW_DATA_DIR / f"{symbol}.json"

        if out_file.exists():
            continue

        print(f"[{i + 1}/{len(stocks)}] Fetching {symbol}...", end="  ")
        data = fetch_stock(symbol)

        if data:
            data["company_name"] = stock["company_name"]
            data["sector"] = stock["sector"]
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(data, f)
            print(f"OK  price={data['price']}  mcap={data['mcap']}  1d={data['returns']['1d']}%")
        else:
            out_file.write_text(json.dumps({"symbol": symbol, "error": True}), encoding="utf-8")
            print("FAILED")

        time.sleep(random.uniform(0.1, 0.3))

    print("\nDone.")


if __name__ == "__main__":
    main()
