# Deploying India Markets Treemap

## Prerequisites

- GitHub account (free)
- Git installed on your machine

---

## Step 1: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. **Repository name**: `india-markets-treemap`
3. **Visibility**: Public
4. **Do NOT** initialize with README or .gitignore — leave blank
5. Click **Create repository**

---

## Step 2: Push Your Local Code

In your terminal, run:

```bash
cd C:/Users/Aditya/Documents/GitHub/finance
git remote add origin https://github.com/YOUR_USERNAME/india-markets-treemap.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages** (in left sidebar)
3. **Source**: Select **Deploy from a branch**
4. **Branch**: Select **main** and folder **/docs**
5. Click **Save**
6. Wait 1-2 minutes — your site will be live at:
   `https://designhawk.github.io/finance/`

---

## Step 4: Trigger First Data Update

1. Go to your repository → **Actions** tab
2. Click **"Daily Market Data Update"** workflow
3. In the right panel, click **"Run workflow"** → **Run workflow**
4. Wait ~5 minutes for it to complete
5. Check the **commits** tab — you should see a new commit "Update market data …"
6. GitHub Pages will auto-deploy from that commit

---

## How It Works

```
Daily at 4:30 PM IST (11:00 UTC)
    │
    ▼
GitHub Actions runs:
  1. get_nifty500.py   → refreshes nifty500.csv
  2. fetch_data.py      → fetches latest prices from Yahoo Finance
   3. build_site_data.py → aggregates to docs/data.json
   4. commits docs/data.json + nifty500.csv
    │
    ▼
GitHub Pages auto-deploys
    │
    ▼
Site updates with new timestamps:
  Market data: <new date/time from data.json>
  Built: <commit timestamp from index.html>
```

---

## Manual Updates

To force an update outside the daily schedule:

1. Go to **Actions** tab
2. Click **"Daily Market Data Update"**
3. Click **"Run workflow"** → **Run workflow**

---

## Adding Cloudflare Analytics (Optional)

1. Create free account at [cloudflare.com/web-analytics](https://cloudflare.com/web-analytics)
2. Add your site domain
3. Copy the 1-line script provided
4. Paste into `docs/index.html` before `</head>`

---

## Troubleshooting

**Site not loading?**
- Check GitHub Pages Settings → ensure source is `main` / `/docs`
- Check Actions tab → see if workflow ran without errors

**Workflow failing?**
- Click on the failed workflow run
- Read the logs to see which step failed
- Most common: rate limiting from Yahoo Finance (wait and retry)

**Timestamps not updating?**
- "Market data" updates when `data.json` is committed
- "Built" updates when a new commit is pushed to `index.html`
- Both should update automatically after each daily run
