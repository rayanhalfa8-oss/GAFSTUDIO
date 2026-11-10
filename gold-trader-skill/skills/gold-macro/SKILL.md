---
name: gold-macro
description: >-
  Gold's macro drivers in one table: US Dollar Index (DXY), US 10-year yield,
  10-year real yield (TIPS), VIX and silver, with 1-day, 5-day and 20-day
  changes, whether each move is usually a tailwind or a headwind for gold,
  and the 60-day correlation with gold. Use when the user asks why gold is
  moving, what the fundamental backdrop is, about the dollar or yields, or
  "علاش الذهب طالع/هابط".
---

# Gold macro drivers

## What to run

```bash
python3 macro.py
python3 macro.py --json
```

Sources: Yahoo Finance chart data (unofficial endpoint, can change) and FRED
(DFII10). Gold here is COMEX futures (GC=F), which trade a few dollars above
spot XAUUSD: use it for direction and % moves, not exact levels.

## How to read it for the user

| driver | usual link to gold |
| --- | --- |
| DXY up | headwind (gold is priced in dollars) |
| 10Y yield up | headwind (holding gold costs more) |
| Real yield up | headwind, the strongest one historically |
| VIX up | tailwind (safe-haven demand) |
| Silver same direction | confirms the move |

1. Lead with the picture: "X tailwinds, Y headwinds over 5 days".
2. Then the one or two drivers that moved most, and why that matters.
3. If gold is moving *against* its drivers (e.g. gold and DXY both up),
   say so: that usually means another force (geopolitics, central-bank
   buying, flows) is in charge.
4. Use the correlation numbers to say how tight the link has been lately
   (e.g. -0.6 with DXY = strong inverse link; near 0 = the link is loose now).

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
