---
name: gold-journal
description: >-
  XAUUSD trading journal and statistics. Logs each trade to gold/journal.csv
  (side, entry, stop, exit, lots, broker P/L, R multiple, session, setup name)
  and measures the strategy with numbers: win rate, average win vs loss,
  profit factor, expectancy, average R, longest losing streak, max drawdown,
  and results by session, weekday and setup. Use when the user wants to log a
  trade, review their results, check if their strategy really works, or
  "سجل الصفقة" / "شنو النتائج ديالي".
---

# Gold journal

## What to run

```bash
python3 journal.py add --side buy --entry 2650 --sl 2645 --exit 2660 --lots 0.2 \
    --pnl 198.4 --open "2026-11-10 10:15" --close "2026-11-10 11:40" --setup "A"
python3 journal.py list --last 10
python3 journal.py stats
python3 journal.py stats --from 2026-11-01 --setup "A"
python3 journal.py today
```

- Prefer `--pnl` from the broker (it includes commission and swap). Without
  it the tool computes P/L from the prices and the contract size.
- The session (Asia / London / NY / overlap) is filled in automatically from
  the open time.
- The setup name is whatever the user calls it. Do not ask what the setup's
  rules are: the user keeps their strategy private.

## How to read the stats with the user

- Under 30 trades: say the sample is too small to judge, every time.
- Profit factor above 1 and positive expectancy = the strategy made money on
  this sample. Above 1.5 is solid.
- Win rate alone means nothing: 40% wins with 1:3 R:R beats 70% wins with
  1:0.3. Explain with their own averages.
- Max losing streak and max drawdown tell the user what to expect
  emotionally and how to size: risk per trade x losing streak should stay
  survivable.
- Point out where results differ clearly by session or weekday, as facts
  ("London: PF 2.1 on 18 trades; New York: PF 0.7 on 12 trades"). The user
  decides what to do with it.

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
