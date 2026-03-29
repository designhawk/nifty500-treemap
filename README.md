# India Markets Treemap

Visualizing the Indian stock market through a treemap — sectors sized by market cap, colored by performance (green = gain, red = loss).

Live at: **https://[username].github.io/[repo]** (GitHub Pages)

## Architecture

```
scripts/get_nifty500.py   → nifty500.csv  (500 stocks + sectors)
fetch_data.py             → raw_data/*.json  (yfinance per-stock data, local only)
build_site_data.py        → site/data.json  (aggregated sector data)
site/index.html           → Treemap frontend
.github/workflows/        → Daily auto-update cron job
```

## Local Setup

```bash
# Install dependencies
uv sync

# Fetch Nifty 500 constituent list from NSE India
uv run python scripts/get_nifty500.py

# Fetch yfinance data for all stocks (~5-10 min)
uv run python fetch_data.py

# Build aggregated site data
uv run python build_site_data.py

# Serve locally
cd site && python -m http.server 8000
```

## GitHub Pages

- Site auto-deploys from the `site/` directory
- Data updates daily at **4:30 PM IST** via GitHub Actions cron
- Workflow: `.github/workflows/daily-update.yml`
- Manual trigger: Go to Actions tab → "Daily Market Data Update" → Run workflow

## Color Layers

Toggle between:
- **1D** — 1-day price change
- **1W** — 1-week price change
- **1M** — 1-month price change

## Drill-down

Click any sector tile to see constituent stocks. Click "← Back to sectors" to return.

## Stats Bar

- **Market cap** — total market capitalization
- **Top gainer** — best performing sector/stock
- **Top loser** — worst performing sector/stock
- **Greed index** — % of stocks gaining (Fear < 25, Neutral < 45, Greed < 70, Extreme ≥ 70)

## Data Source

- Stock list: NSE India official API
- Price/market cap: Yahoo Finance (yfinance Python library)
- Free, no API key required
