# Sepang Ticket Monitor

Monitors F1 ticket availability for the **2026 Bahrain Grand Prix in Malaysia (Sepang)** and sends a Telegram alert when tickets go on sale.

## What it monitors

| Site | URL | Trigger |
|------|-----|---------|
| Sepang Circuit | `sepangcircuit.com/ticketing` | Any F1 card with a "Buy Ticket" button |
| F1 Ticket Store | `tickets.formula1.com/en` | Bahrain GP 2026 card changes to "Book Now" |

## How it works

1. GitHub Actions runs `monitor.py` every 5 minutes (only one run at a time — concurrent runs are cancelled)
2. Each scraper fetches its target page and returns the relevant ticket card
3. If the result differs from the last saved state, a Telegram message is sent
4. Updated state is committed back to `state.json`
5. Each job has a 10-minute timeout to prevent stuck runs

## Setup

### 1. Fork this repo

### 2. Add GitHub Actions secrets

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Description |
|--------|-------------|
| `BOT_TOKEN` | Telegram bot token from [@BotFather](https://t.me/BotFather) |
| `CHAT_ID` | Telegram chat ID to send alerts to |

### 3. Enable GitHub Actions

The workflow runs automatically on a `*/5 * * * *` cron schedule. You can also trigger it manually via **Actions → Sepang Ticket Monitor → Run workflow**.

## Project structure

```
monitor.py          # Orchestrator — runs all checkers, diffs state, sends alerts
config.py           # Site URLs, button text, and keywords per site
state.py            # Load/save state.json (atomic writes)
telegram.py         # Telegram Bot API wrapper
monitors/
  sepang.py         # Scraper for sepangcircuit.com
  f1tickets.py      # Scraper for tickets.formula1.com (Bahrain GP 2026 only)
.github/
  workflows/
    monitor.yml     # GitHub Actions cron workflow
state.json          # Last known state (committed by the workflow)
```
