---
name: gold-risk
description: >-
  Pre-trade risk check for XAUUSD. Checks a planned trade against the user's
  own limits and prints PASS / WARN / BLOCK: risk per trade, reward:risk,
  trades already taken today, today's loss limit, high-impact USD news inside
  the blackout window, spread, and market hours. It checks money and timing
  rules only, never the setup. Use before a trade, or when the user asks
  "واش ندخل دابا" in terms of risk, news or limits.
---

# Gold risk check

## What to run

```bash
python3 check.py --entry 2650 --sl 2645 --lots 0.2 --tp 2660 --spread 0.3
python3 check.py --entry 2650 --sl 2645 --lots 0.2 --at "2026-11-12 14:20"
```

It reads:
- `gold/config.json` for the limits (`max_risk_percent`, `min_rr`,
  `max_trades_per_day`, `max_daily_loss_percent`, `news_blackout_minutes`,
  `max_spread`, `account_balance`),
- `gold/journal.csv` (from /gold-journal) for today's trades and P/L,
- `gold/calendar.json` (from /gold-econ) for news times. Run /gold-econ first
  if it is missing or older than a day.

## How to answer

- Lead with the verdict. For each BLOCK, the reason in one line.
- Never override a BLOCK and never suggest bending the user's own limits.
  If the user wants to change a limit, they change `gold/config.json`
  themselves, outside a trade.
- "PASS" means the trade fits the limits. It says nothing about whether the
  setup is good. Say that if the user seems to read it as a green light.

## Rules for every gold skill

- **Answer in the user's language.** If they write in Moroccan Darija, answer in
  Darija (Arabic script); Arabic, French or English likewise. Keep numbers,
  times and tickers as digits.
- **Never touch the user's strategy.** Do not suggest entries, exits, buy/sell
  calls or changes to their rules unless they ask. These tools give context
  (news, drivers, positioning, risk arithmetic), not signals.
- **Say "usually", not "will".** Each relationship (dollar up -> gold down...)
  is a tendency that breaks often. Never promise an outcome.
- **Name the source and its age** (e.g. "CFTC, positions of Tuesday 4 Nov").
  If a tool fails, say which part is missing; never fill the gap with guesses
  or invented numbers.
- **Data lives in `gold/`** in the working folder (override with the
  `GOLD_DIR` environment variable). Settings are in `gold/config.json`; copy
  `config.example.json` from the gold-brief skill folder if it is missing.
- Run the script by its full path (it sits in the same folder as this
  SKILL.md), from the user's working folder, so `gold/` is created there.
  `python3` 3.9+, standard library only, nothing to install.
- Not financial advice: say so once when you give a market summary, briefly.
