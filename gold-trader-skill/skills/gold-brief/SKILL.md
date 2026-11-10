---
name: gold-brief
description: >-
  The daily gold (XAUUSD) fundamental brief. Runs the other gold tools
  (market clock, economic calendar, macro drivers, CFTC positioning, news)
  and writes one short summary in the user's language: today's news and
  when to stay out, the dollar/yields backdrop, what the funds hold, and the
  headlines that matter. Ready to copy into WhatsApp. Never gives buy/sell
  calls. Use when the user asks for the daily brief, "الخلاصة ديال اليوم",
  "brief", a morning summary, or what they need to know before trading gold.
---

# Daily gold brief

## What to run

```bash
python3 brief.py                 # everything; saves gold/brief-YYYY-MM-DD.json
python3 brief.py --skip cot      # skip a part
```

It needs the other gold skills installed next to it (same parent folder).
Parts that fail are listed under `unavailable`; say which ones and carry on
with the rest. If `gold/config.json` is missing, copy `config.example.json`
from this folder to `gold/config.json` and ask the user for their timezone,
balance and limits.

## The brief: fixed structure, in the user's language

Keep it under ~25 lines, phone-sized. Example skeleton in Darija:

```
🟡 *خلاصة الذهب — الثلاثاء 10 نونبر*

⏰ *السوق:* مفتوح — دابا جلسة لندن. التداخل لندن/نيويورك من 13:00 حتى 16:00.

📅 *الأخبار ديال اليوم (ساعة المغرب):*
• 14:30 CPI (التضخم) — المتوقع 0.3% / السابق 0.4%
  ⛔ بعد من الدخول 14:15 → 14:45
(إلا ما كاين والو: "ما كاين حتى خبر قوي اليوم")

💵 *الدولار والعوائد (5 أيام):*
DXY ‎+0.4% (ضغط على الذهب) • العائد 10 سنين ‎-6bp (دعم) • VIX ‎+8% (دعم)
→ 2 داعمين، 1 ضاغط

🏦 *الكبار (COT، مراكز الثلاثاء):*
الصناديق شاريين صافي 180,000 عقد، زادو 12,000 هاد الأسبوع — قريبين من أعلى مستوى ف3 سنين (مزدحم).

📰 *أهم الأخبار:*
• ...
• ...

⚠️ هادي معلومات، ماشي توصية بالشراء ولا البيع.
```

Rules for the brief:
- Facts and usual effects only. No "buy", "sell", "target", or bias call
  such as "gold will go up today".
- Every number comes from the tool output. If a part is unavailable, write
  one line saying so instead of the section.
- Times in the user's timezone, 24-hour clock.
- WhatsApp formatting: `*bold*`, emojis as section markers, no tables, no
  links unless the user asks. Give it as one block they can copy. You
  cannot send WhatsApp messages yourself; say so if asked, and hand over the
  block.
- Save the final text next to the JSON as `gold/brief-YYYY-MM-DD.md`.

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
