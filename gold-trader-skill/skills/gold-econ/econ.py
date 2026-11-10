#!/usr/bin/env python3
"""Economic calendar for gold traders (the week's USD news that moves XAUUSD).

Source: the free weekly JSON feed behind Forex Factory's calendar
(nfs.faireconomy.media). It is cached in gold/ for one hour so the feed is not
hammered. Times are shown in your own timezone, each event is tagged (Fed,
Inflation, Jobs, Growth...) with how it usually touches gold, and the
"news blackout" window around it is written to gold/calendar.json so
/gold-risk can warn you before a trade.

    python3 econ.py week                      # this week, high impact, USD
    python3 econ.py week --impact medium      # medium and high
    python3 econ.py week --next               # next week
    python3 econ.py today
    python3 econ.py next                      # the next high-impact event + countdown
    python3 econ.py week --file feed.json     # read a saved feed instead
"""
import argparse
import gzip
import json
import os
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

UTC = timezone.utc
UA = "Mozilla/5.0 (gold-trader-skill; +https://github.com)"
FEEDS = {
    "this": "https://nfs.faireconomy.media/ff_calendar_thisweek.json",
    "next": "https://nfs.faireconomy.media/ff_calendar_nextweek.json",
}
DEFAULTS = {"timezone": "Africa/Casablanca", "news_blackout_minutes": 15}
IMPACT_RANK = {"Holiday": 0, "Non-Economic": 0, "Low": 1, "Medium": 2, "High": 3}

# (tag, keywords, how it usually touches gold)
TAGS = [
    ("Fed", ["fomc", "federal funds", "fed chair", "powell", "fed ", "monetary policy",
             "rate decision", "interest rate", "beige book"],
     "Hawkish (rates higher for longer) usually weighs on gold; dovish (cuts) usually supports it."),
    ("Inflation", ["cpi", "pce", "ppi", "inflation", "price index"],
     "Hotter than forecast -> higher rate expectations -> usually pressure on gold short term; cooler -> usually supportive."),
    ("Jobs", ["non-farm", "nonfarm", "nfp", "unemployment", "jobless", "adp", "employment", "jolts", "payrolls", "earnings"],
     "Strong jobs -> stronger dollar and yields -> usually a headwind; weak jobs -> usually supportive."),
    ("Growth", ["gdp", "retail sales", "ism", "pmi", "durable goods", "industrial production", "consumer confidence", "sentiment"],
     "Strong data -> dollar/yields up -> usually a headwind; weak data -> usually supportive."),
    ("Speech", ["speaks", "testifies", "speech", "press conference"],
     "Watch for hints on rates: hawkish tone weighs on gold, dovish tone supports it."),
]


# ---------------------------------------------------------------- helpers
def data_dir():
    d = Path(os.environ.get("GOLD_DIR", "gold"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_config():
    cfg = dict(DEFAULTS)
    p = data_dir() / "config.json"
    if p.exists():
        cfg.update(json.loads(p.read_text(encoding="utf-8")))
    return cfg


def local_tz(name):
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(name)
    except Exception:
        import sys
        print(f"note: timezone '{name}' not found (try: pip install tzdata); using this computer's local time",
              file=sys.stderr)
        return datetime.now().astimezone().tzinfo


def http_get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
    return raw.decode("utf-8", "replace")


def parse_time(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(UTC)


# ---------------------------------------------------------------- core
def tag_event(title):
    t = " " + title.lower() + " "
    for tag, words, note in TAGS:
        if any(w in t for w in words):
            return tag, note
    return "Other", "Can move the dollar, and through it, gold."


def fetch_feed(which="this", file=None, max_age=3600):
    if file:
        return Path(file).read_text(encoding="utf-8")
    cache = data_dir() / f"ff_{which}week.json"
    if cache.exists() and time.time() - cache.stat().st_mtime < max_age:
        return cache.read_text(encoding="utf-8")
    text = http_get(FEEDS[which])
    json.loads(text)  # refuse to cache an error page
    cache.write_text(text, encoding="utf-8")
    return text


def parse_events(text, currencies=("USD",), min_impact="High"):
    floor = IMPACT_RANK.get(min_impact.capitalize(), 3)
    out = []
    for e in json.loads(text):
        cur = (e.get("country") or "").upper()
        if currencies and cur not in currencies:
            continue
        impact = e.get("impact") or "Low"
        if IMPACT_RANK.get(impact, 0) < floor:
            continue
        try:
            when = parse_time(e["date"])
        except (KeyError, ValueError):
            continue
        tag, note = tag_event(e.get("title", ""))
        out.append({
            "title": e.get("title", ""),
            "currency": cur,
            "impact": impact,
            "time_utc": when.isoformat(),
            "forecast": e.get("forecast") or "",
            "previous": e.get("previous") or "",
            "actual": e.get("actual") or "",
            "tag": tag,
            "gold_note": note,
        })
    out.sort(key=lambda x: x["time_utc"])
    return out


def write_cache(events, blackout):
    p = data_dir() / "calendar.json"
    p.write_text(json.dumps({"updated_utc": datetime.now(UTC).isoformat(),
                             "blackout_minutes": blackout, "events": events},
                            indent=2, ensure_ascii=False), encoding="utf-8")
    return p


def countdown(delta):
    mins = int(delta.total_seconds() // 60)
    if mins < 0:
        return "passed"
    d, rem = divmod(mins, 1440)
    h, m = divmod(rem, 60)
    return (f"{d}d " if d else "") + f"{h}h{m:02d}"


def show(events, tz, blackout, now):
    if not events:
        print("No events match (try --impact medium or --next).")
        return
    day = None
    for e in events:
        t = parse_time(e["time_utc"]).astimezone(tz)
        if t.date() != day:
            day = t.date()
            print(f"\n=== {t.strftime('%A %d %b %Y')} ===")
        fc = f"  forecast {e['forecast']}" if e["forecast"] else ""
        pv = f"  previous {e['previous']}" if e["previous"] else ""
        ac = f"  ACTUAL {e['actual']}" if e["actual"] else ""
        when = parse_time(e["time_utc"])
        flag = "  <- NOW (blackout)" if abs((when - now).total_seconds()) <= blackout * 60 else ""
        print(f"{t.strftime('%H:%M')}  [{e['impact']:<6}] {e['currency']} {e['title']}  ({e['tag']}){fc}{pv}{ac}{flag}")
        print(f"        gold: {e['gold_note']}")
        a = (t - timedelta(minutes=blackout)).strftime("%H:%M")
        b = (t + timedelta(minutes=blackout)).strftime("%H:%M")
        print(f"        avoid new entries {a} -> {b}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", nargs="?", default="week", choices=["week", "today", "next"])
    ap.add_argument("--next", action="store_true", help="next week's calendar")
    ap.add_argument("--impact", default="high", choices=["high", "medium", "low"])
    ap.add_argument("--currency", default="USD", help="comma list, or ALL (default USD)")
    ap.add_argument("--file", help="read a saved feed JSON instead of downloading")
    ap.add_argument("--tz", help="IANA timezone (default from gold/config.json)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    cfg = load_config()
    tz = local_tz(a.tz or cfg["timezone"])
    blackout = int(cfg["news_blackout_minutes"])
    curs = () if a.currency.upper() == "ALL" else tuple(c.strip().upper() for c in a.currency.split(","))
    events = parse_events(fetch_feed("next" if a.next else "this", a.file), curs, a.impact)
    if not a.next:
        write_cache(parse_events(fetch_feed("this", a.file), ("USD",), "high"), blackout)

    now = datetime.now(UTC)
    if a.cmd == "today":
        today = now.astimezone(tz).date()
        events = [e for e in events if parse_time(e["time_utc"]).astimezone(tz).date() == today]
    elif a.cmd == "next":
        events = [e for e in events if parse_time(e["time_utc"]) >= now - timedelta(minutes=blackout)][:1]
        if events:
            print(f"Next: in {countdown(parse_time(events[0]['time_utc']) - now)}")

    if a.json:
        print(json.dumps(events, indent=2, ensure_ascii=False))
    else:
        show(events, tz, blackout, now)


if __name__ == "__main__":
    main()
