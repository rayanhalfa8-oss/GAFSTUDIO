#!/usr/bin/env python3
"""Gold news monitor: headlines that move XAUUSD, grouped by theme.

Source: Google News RSS searches (free, no key). Each headline is tagged
(Gold, Fed, Inflation, Jobs, Dollar, Geopolitics, Central banks) and duplicates
across searches are merged. With --new, only headlines not seen at the last
check are shown (state in gold/news_seen.json).

    python3 news.py                    # last 24 h
    python3 news.py --hours 6 --new
    python3 news.py --query "gold ETF flows" --query "China gold demand"
    python3 news.py --file saved.xml   # parse a saved RSS file
"""
import argparse
import gzip
import json
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

UTC = timezone.utc
UA = "Mozilla/5.0 (gold-trader-skill)"
DEFAULT_QUERIES = [
    "gold price",
    "XAUUSD",
    "Federal Reserve interest rates",
    "US inflation CPI",
    "US dollar index",
    "central bank gold buying",
    "geopolitical tensions markets",
]
TAGS = [
    ("Gold", ["gold", "xau", "bullion", "precious metal"]),
    ("Fed", ["fed", "federal reserve", "fomc", "powell", "rate cut", "rate hike", "interest rate"]),
    ("Inflation", ["inflation", "cpi", "pce", "ppi", "price index"]),
    ("Jobs", ["jobs", "payroll", "nfp", "unemployment", "labor market", "jobless"]),
    ("Dollar", ["dollar", "dxy", "greenback", "treasury yield", "bond yield", "yields"]),
    ("Geopolitics", ["war", "attack", "missile", "sanction", "tension", "conflict", "ceasefire", "election", "tariff"]),
    ("Central banks", ["central bank", "pboc", "reserves", "ecb", "boj"]),
]


def data_dir():
    d = Path(os.environ.get("GOLD_DIR", "gold"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def http_get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
    return raw.decode("utf-8", "replace")


def rss_url(query, hours):
    when = "1d" if hours <= 24 else f"{max(1, hours // 24)}d"
    q = urllib.parse.quote(f"{query} when:{when}")
    return f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"


def tags_for(title):
    t = title.lower()
    out = [tag for tag, words in TAGS if any(re.search(r"\b" + re.escape(w) + r"s?\b", t) for w in words)]
    return out or ["Other"]


def parse_rss(text):
    items = []
    root = ET.fromstring(text)
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        src = it.find("source")
        source = (src.text or "").strip() if src is not None else ""
        if source and title.endswith(" - " + source):
            title = title[: -len(" - " + source)]
        try:
            when = parsedate_to_datetime(it.findtext("pubDate") or "").astimezone(UTC)
        except (TypeError, ValueError):
            continue
        items.append({"title": title, "source": source, "link": (it.findtext("link") or "").strip(),
                      "time_utc": when.isoformat(), "tags": tags_for(title)})
    return items


def norm(title):
    return re.sub(r"[^a-z0-9 ]", "", title.lower())[:80]


def collect(texts, hours, now=None):
    now = now or datetime.now(UTC)
    cutoff = now - timedelta(hours=hours)
    seen, out = set(), []
    for text in texts:
        for it in parse_rss(text):
            k = norm(it["title"])
            if k in seen or datetime.fromisoformat(it["time_utc"]) < cutoff:
                continue
            seen.add(k)
            out.append(it)
    out.sort(key=lambda x: x["time_utc"], reverse=True)
    return out


def only_new(items):
    p = data_dir() / "news_seen.json"
    seen = set(json.loads(p.read_text(encoding="utf-8"))) if p.exists() else set()
    fresh = [i for i in items if norm(i["title"]) not in seen]
    seen |= {norm(i["title"]) for i in items}
    p.write_text(json.dumps(sorted(seen)[-2000:]), encoding="utf-8")
    return fresh


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hours", type=int, default=24)
    ap.add_argument("--query", action="append", help="extra search (repeatable); replaces the defaults")
    ap.add_argument("--new", action="store_true", help="only headlines not shown at the last check")
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--file", action="append", help="saved RSS file(s) instead of downloading")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.file:
        texts = [Path(f).read_text(encoding="utf-8") for f in a.file]
    else:
        texts, errors = [], []
        for q in a.query or DEFAULT_QUERIES:
            try:
                texts.append(http_get(rss_url(q, a.hours)))
            except Exception as e:  # one dead search should not kill the rest
                errors.append(f"{q}: {e}")
        for e in errors:
            print(f"warning: {e}")
    items = collect(texts, a.hours)
    if a.new:
        items = only_new(items)
    items = items[: a.limit]

    if a.json:
        print(json.dumps(items, indent=2, ensure_ascii=False))
        return
    if not items:
        print("No new headlines.")
        return
    for it in items:
        t = datetime.fromisoformat(it["time_utc"]).strftime("%d %b %H:%M UTC")
        print(f"{t}  [{', '.join(it['tags'])}] {it['title']}  - {it['source']}")
        print(f"         {it['link']}")


if __name__ == "__main__":
    main()
