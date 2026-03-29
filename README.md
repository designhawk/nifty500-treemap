# Nifty 500 Treemap

Nifty 500 stock market treemap — sectors sized by market cap, colored by gain/loss. Drill-down by sector, toggle 1D/1W/1M views, dark/light mode.

**Live at: https://finance-4yc.pages.dev** (Cloudflare Pages)

---

## Architecture

```
scripts/get_nifty500.py   → nifty500.csv  (500 stocks + sectors)
fetch_data.py             → raw_data/*.json  (yfinance per-stock data, local only)
build_site_data.py        → docs/data.json  (aggregated sector data)
docs/index.html           → Treemap frontend
.github/workflows/        → Daily auto-update cron → Cloudflare Pages deploy
```

---

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
cd docs && python -m http.server 8000
```

---

## Deployment

- Hosted on **Cloudflare Pages** — auto-deployed via GitHub Actions on each push to `master`
- Data updates daily at **4:30 PM IST** (11:00 UTC) via GitHub Actions cron
- Workflow: `.github/workflows/daily-update.yml`
- Manual trigger: Actions tab → "Daily Market Data Update" → Run workflow

---

## Security

- `CLOUDFLARE_API_TOKEN` is stored as an encrypted GitHub Actions secret — never hardcoded
- Secret scanning and push protection enabled on this repo
- No API keys or credentials in source code
- `.gitignore` excludes raw data, virtual envs, and wrangler cache

---

## Features

**Treemap** — Squarified layout, area proportional to market cap. Solid green = gainers, solid red = losers, white text.

**Drill-down** — Click any sector tile to see constituent stocks. Back button to return.

**Time toggle** — 1D / 1W / 1M buttons switch the color period; stats bar always reflects the active period.

**Stats bar** — Total market cap, top gainer (green), top loser (red), Greed Index (colored 0–100).

**Greed Index** — % of stocks gaining. Fear < 25 | Neutral < 45 | Greed < 70 | Extreme ≥ 70.

**Theme** — Dark (default) and light mode toggle via CSS custom properties.

**WCAG accessible** — Font sizes ≥ 12px, contrast ≥ 4.5:1, touch targets ≥ 24px, no zoom blocking.

---

## Data Source

- Stock list: NSE India official API
- Price/market cap: Yahoo Finance (yfinance)
- Free, no API key required
