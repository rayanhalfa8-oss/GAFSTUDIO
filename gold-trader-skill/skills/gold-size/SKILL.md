---
name: gold-size
description: >-
  XAUUSD position size calculator. From the user's balance, risk (percent or
  dollars), entry and stop-loss, gives the lot size, the real loss at the
  stop, the value of a 1$ move, the margin estimate, the reward:risk if a
  take-profit is given, and price targets at 1R/1.5R/2R/3R. Handles buys and
  sells, minimum lot and lot step. Use when the user asks how many lots,
  "شحال من لوت", position size, or how much they lose if the stop hits.
---

# Gold position size

## What to run

```bash
python3 size.py --entry 2650.5 --sl 2645.5                    # balance & risk from config
python3 size.py --balance 1000 --risk 1 --entry 2650 --sl 2656 --tp 2638
python3 size.py --balance 500 --risk-money 5 --entry 2650 --sl-distance 3 --side buy
```

Defaults come from `gold/config.json`: `account_balance`, `risk_percent`,
`contract_size` (100 oz per lot at most brokers), `min_lot`, `lot_step`,
`leverage`.

## How to answer

- Give the lot size first, big and clear, then the loss at the stop in $
  and in % of the balance.
- The entry, stop and target come from the user's strategy. Do not propose
  other levels.
- If the minimum lot already risks more than the budget, say so plainly:
  the account is too small for that stop distance.
- Points vs dollars: 1$ in the gold price = 100 points on 2-decimal
  brokers. Brokers name "pips" differently; trust dollars.
- Remind once, if relevant: the contract size must match the broker's
  (check the symbol's specification in MT4/MT5).

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
