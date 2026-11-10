---
name: gold-news
description: >-
  Gold news monitor. Pulls the last hours of headlines that move XAUUSD
  (gold price, Fed and rates, inflation, jobs, the dollar and yields,
  geopolitics, central-bank gold buying) from Google News, merges duplicates,
  tags each by theme and, with --new, shows only what appeared since the last
  check. Use when the user asks for gold news, "what's moving gold", "شنو
  الأخبار ديال الذهب", or wants a summary of the news from links they send.
---

# Gold news

## What to run

```bash
python3 news.py                      # last 24 h, all default searches
python3 news.py --hours 6 --new      # only what is new since last time
python3 news.py --query "gold ETF" --query "China gold demand"
python3 news.py --json
```

## How to answer

1. Group headlines by theme (Fed, Inflation, Dollar, Geopolitics, Gold...).
   Drop duplicates and pure noise (price-recap articles that say nothing new).
2. For each theme, one or two sentences in the user's language: what
   happened, and how it usually touches gold. Quote no more than the headline.
3. End with the 2-3 points that matter most today.
4. Headlines are not verified facts. If something big is in only one
   headline, say so.

## When the user sends links instead

If the user gives URLs and says what they need from them, read each page
(with your web tools), and summarise exactly that: the facts, the numbers,
the date, and the usual effect on gold. If a site blocks automated reading,
ask the user to paste the text or send a screenshot. Never invent the
content of a page you could not read.

## Sharing on WhatsApp

You cannot send WhatsApp messages. When the user wants to share, give the
summary as one ready-to-copy block in WhatsApp formatting: `*bold*`, short
lines, emojis as section markers (📰 🏦 💵 ⚠️), no tables.

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
