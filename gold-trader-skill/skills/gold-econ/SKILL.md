---
name: gold-econ
description: >-
  Economic calendar for gold (XAUUSD) traders. Lists this week's or next
  week's high-impact USD news (FOMC, CPI, NFP, PCE, GDP, Powell speeches...)
  in the user's own timezone, tags each event (Fed, Inflation, Jobs, Growth),
  explains how it usually moves gold, gives the "avoid new entries" window
  around it, and saves the times to gold/calendar.json for /gold-risk. Use when
  the user asks what news is coming, when NFP/CPI/FOMC is, whether there is
  news today, or "واش كاين شي خبر اليوم".
---

# Gold economic calendar

## What to run

```bash
python3 econ.py today                 # today's high-impact USD events
python3 econ.py week                  # the whole week
python3 econ.py week --impact medium  # include medium impact
python3 econ.py week --next           # next week (published late in the week)
python3 econ.py next                  # the next event and a countdown
python3 econ.py week --json           # for your own processing
```

The feed is Forex Factory's free weekly JSON. It is cached for one hour in
`gold/`; do not loop on it. If it fails (blocked network, site change), say
so and offer: the user can paste the calendar text or a screenshot and you
summarise that instead.

## How to answer

1. One line per event: local time, name, forecast vs previous.
2. Under it, in the user's language, what it usually does to gold (the
   `gold_note`), and the window to avoid new entries (blackout, default
   +/-15 minutes, set `news_blackout_minutes` in `gold/config.json`).
3. Flag the big ones first: FOMC decision and press conference, CPI, NFP,
   PCE. On those days spreads widen and price can spike both ways.
4. If an `actual` value is present, compare it with the forecast: above or
   below, and what that usually means for gold.

Example (Darija):

> **الخميس 14:30** — CPI m/m (التضخم) — المتوقع 0.3% / السابق 0.4%
> إلا خرج أعلى من المتوقع، غالباً كيضغط على الذهب حيت كيطلع احتمال بقاء الفائدة مرتفعة. إلا خرج أقل، غالباً كيدعمو.
> ⛔ بعد من الدخول بين 14:15 و 14:45.

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
