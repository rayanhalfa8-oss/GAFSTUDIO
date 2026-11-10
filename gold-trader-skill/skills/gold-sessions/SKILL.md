---
name: gold-sessions
description: >-
  Gold market clock. Says whether XAUUSD is open, closed for the weekend or
  in the daily 17:00-18:00 New York break, which session is active (Asia,
  London, New York, London+NY overlap), and today's session times in the
  user's own timezone with daylight-saving handled. Use when the user asks if
  the market is open, when London or New York opens, or "إمتى كتحل لندن".
---

# Gold sessions

## What to run

```bash
python3 sessions.py
python3 sessions.py --at "2026-11-12 14:30"
python3 sessions.py --tz Africa/Casablanca --json
```

Times are in the timezone from `gold/config.json` (`timezone`, default
`Africa/Casablanca`). If Python has no timezone database (some Windows
installs), the computer's local time is used instead; if times look shifted,
suggest `pip install tzdata`.

## How to answer

- State open/closed and the active session first.
- Then today's schedule in local time. The London+NY overlap is usually the
  most liquid and volatile window for gold; Asia is usually the quietest.
- US and UK bank holidays are not in the tool: mention it on those dates.

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
