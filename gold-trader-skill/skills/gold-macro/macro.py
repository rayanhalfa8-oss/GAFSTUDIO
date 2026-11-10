#!/usr/bin/env python3
"""Gold's macro drivers in one table: dollar, yields, real yields, fear, silver.

For each driver it shows the last value and its 1-day / 5-day / 20-day change,
and whether that move is usually a TAILWIND or a HEADWIND for gold. This is
context, not a signal: it says what the backdrop is, never when to trade.

Sources (free, no key): Yahoo Finance chart endpoint (unofficial, can change)
for gold futures, DXY, US 10Y yield, VIX and silver; FRED for the 10-year real
yield (DFII10, TIPS).

    python3 macro.py
    python3 macro.py --json
"""
import argparse
import csv
import gzip
import io
import json
import math
import urllib.parse
import urllib.request
from datetime import datetime, timezone

UTC = timezone.utc
UA = "Mozilla/5.0 (gold-trader-skill)"

# symbol, name, relation to gold (+1 moves with gold, -1 against), unit, threshold for 5d move
DRIVERS = [
    ("GC=F", "Gold futures (COMEX)", 0, "$", 0),
    ("DX-Y.NYB", "US Dollar Index (DXY)", -1, "pct", 0.3),
    ("^TNX", "US 10Y yield", -1, "bp", 5),
    ("^VIX", "VIX (fear index)", +1, "pct", 5),
    ("SI=F", "Silver futures", +1, "pct", 1.0),
]
FRED_REAL = ("DFII10", "US 10Y real yield (TIPS)", -1, "bp", 5)
WHY = {
    "DX-Y.NYB": "gold is priced in dollars: a stronger dollar usually pushes it down",
    "^TNX": "higher yields raise the cost of holding gold, which pays nothing",
    "DFII10": "real yields are gold's closest driver: up = headwind, down = tailwind",
    "^VIX": "fear tends to bring safe-haven buying",
    "SI=F": "silver moving the same way confirms the metals move",
}


def http_get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
    return raw.decode("utf-8", "replace")


def yahoo_url(sym):
    return f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(sym)}?range=6mo&interval=1d"


def parse_yahoo(text):
    """-> list of (date 'YYYY-MM-DD', close), oldest first, gaps dropped."""
    res = json.loads(text)["chart"]["result"][0]
    ts = res.get("timestamp") or []
    closes = res["indicators"]["quote"][0].get("close") or []
    out = []
    for t, c in zip(ts, closes):
        if c is not None:
            out.append((datetime.fromtimestamp(t, UTC).strftime("%Y-%m-%d"), float(c)))
    return out


def parse_fred(text):
    rows = list(csv.reader(io.StringIO(text)))
    out = []
    for r in rows[1:]:
        if len(r) >= 2 and r[1] not in ("", "."):
            try:
                out.append((r[0], float(r[1])))
            except ValueError:
                pass
    return out


def change(series, n, unit):
    if len(series) <= n:
        return None
    a, b = series[-1 - n][1], series[-1][1]
    if unit == "bp":
        return round((b - a) * 100, 1)
    if unit == "$":
        return round(b - a, 2)
    return round((b / a - 1) * 100, 2) if a else None


def corr(xs, ys):
    n = len(xs)
    if n < 10:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return round(sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy), 2) if sx and sy else None


def returns_by_date(series):
    return {series[i][0]: series[i][1] / series[i - 1][1] - 1 for i in range(1, len(series)) if series[i - 1][1]}


def rolling_corr(a, b, days=60):
    ra, rb = returns_by_date(a), returns_by_date(b)
    common = sorted(set(ra) & set(rb))[-days:]
    return corr([ra[d] for d in common], [rb[d] for d in common])


def verdict(rel, unit, thr, chg5):
    if rel == 0 or chg5 is None:
        return ""
    if abs(chg5) < thr:
        return "neutral"
    return "TAILWIND" if (chg5 > 0) == (rel > 0) else "HEADWIND"


def build(series_by_sym):
    rows = []
    for sym, name, rel, unit, thr in DRIVERS + [FRED_REAL]:
        s = series_by_sym.get(sym)
        if not s:
            rows.append({"symbol": sym, "name": name, "error": "no data"})
            continue
        c5 = change(s, 5, unit)
        rows.append({
            "symbol": sym, "name": name, "date": s[-1][0], "last": round(s[-1][1], 3),
            "unit": unit, "chg_1d": change(s, 1, unit), "chg_5d": c5, "chg_20d": change(s, 20, unit),
            "for_gold": verdict(rel, unit, thr, c5), "why": WHY.get(sym, ""),
        })
    gold = series_by_sym.get("GC=F")
    corrs = {}
    if gold:
        for sym in ("DX-Y.NYB", "^TNX", "SI=F"):
            if series_by_sym.get(sym):
                corrs[sym] = rolling_corr(gold, series_by_sym[sym])
    tail = sum(r.get("for_gold") == "TAILWIND" for r in rows)
    head = sum(r.get("for_gold") == "HEADWIND" for r in rows)
    return {"drivers": rows, "corr_60d_with_gold": corrs,
            "summary": {"tailwinds": tail, "headwinds": head},
            "note": "Context only. Gold futures (GC=F) trade a few dollars above spot XAUUSD."}


def fetch_all():
    data, errors = {}, []
    for sym, *_ in DRIVERS:
        try:
            data[sym] = parse_yahoo(http_get(yahoo_url(sym)))
        except Exception as e:
            errors.append(f"{sym}: {e}")
    try:
        data["DFII10"] = parse_fred(http_get("https://fred.stlouisfed.org/graph/fredgraph.csv?id=DFII10"))[-130:]
    except Exception as e:
        errors.append(f"DFII10: {e}")
    return data, errors


def fmt(v, unit):
    if v is None:
        return "-"
    if unit == "bp":
        return f"{v:+.1f}bp"
    if unit == "$":
        return f"{v:+.2f}$"
    return f"{v:+.2f}%"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    data, errors = fetch_all()
    out = build(data)
    out["errors"] = errors
    if a.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return
    print(f"{'driver':<28}{'last':>10}{'1d':>11}{'5d':>11}{'20d':>11}  for gold")
    for r in out["drivers"]:
        if "error" in r:
            print(f"{r['name']:<28}  (no data)")
            continue
        print(f"{r['name']:<28}{r['last']:>10}{fmt(r['chg_1d'], r['unit']):>11}"
              f"{fmt(r['chg_5d'], r['unit']):>11}{fmt(r['chg_20d'], r['unit']):>11}  {r['for_gold']}")
    s = out["summary"]
    print(f"\n5-day backdrop: {s['tailwinds']} tailwind(s), {s['headwinds']} headwind(s).")
    if out["corr_60d_with_gold"]:
        print("60-day correlation with gold: " + ", ".join(f"{k} {v}" for k, v in out["corr_60d_with_gold"].items()))
    print(out["note"])
    for e in errors:
        print(f"warning: {e}")


if __name__ == "__main__":
    main()
