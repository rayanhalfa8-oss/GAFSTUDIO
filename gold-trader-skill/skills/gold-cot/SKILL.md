---
name: gold-cot
description: >-
  What the big players hold in gold: reads the CFTC Commitments of Traders
  report for COMEX gold and shows the funds' (large speculators') net long,
  its weekly change, its share of open interest, commercials' net position,
  and where funds' positioning sits in its 3-year range (crowded long or
  light). The gold version of following the smart money. Use when the user
  asks about COT, institutional positioning, what funds or banks are doing in
  gold, or "شنو كيديرو الكبار فالذهب".
---

# Gold COT positioning

## What to run

```bash
python3 cot.py               # latest report + 6 weeks of history
python3 cot.py --weeks 12
python3 cot.py --json
```

Source: CFTC public reporting API, Legacy futures-only report, gold code
088691. Positions are as of **Tuesday**, published **Friday** afternoon US
time. If the field names changed, the script says which are missing; tell
the user the source changed rather than guessing numbers.

## How to explain it

1. Funds net long and its weekly change: are they adding or cutting?
2. The 3-year percentile:
   - 85+ = crowded long: a lot of buying is already done; sharp drops can
     come from funds exiting.
   - 15 or less = light: funds have room to buy.
   - in between = no extreme.
3. Commercials are usually net short (producers hedge); that is normal, not
   bearish by itself.
4. Always add: this is weekly, delayed positioning. It describes the
   backdrop; it does not time entries.

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
