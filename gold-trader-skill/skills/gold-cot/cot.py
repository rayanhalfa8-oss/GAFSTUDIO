#!/usr/bin/env python3
"""What the big players hold in gold: the CFTC Commitments of Traders report.

Every Friday (for positions as of Tuesday) the CFTC publishes who is long and
short COMEX gold futures. This reads the Legacy report for gold (contract code
088691) and shows:
  - large speculators (funds, "non-commercials"): net long, weekly change
  - commercials (producers, banks hedging): net position
  - where the funds' net long sits within the last 3 years (percentile):
    near 100 = crowded long, near 0 = very light positioning

Source: CFTC public reporting API (free, no key). The data is 3 days old when it
is published: it describes positioning, it does not time trades.

    python3 cot.py
    python3 cot.py --weeks 8 --json
    python3 cot.py --file saved.json
"""
import argparse
import gzip
import json
import urllib.parse
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (gold-trader-skill)"
DATASET = "https://publicreporting.cftc.gov/resource/6dca-aqww.json"
GOLD_CODE = "088691"
F = {  # Legacy futures-only field names
    "date": "report_date_as_yyyy_mm_dd",
    "oi": "open_interest_all",
    "nc_long": "noncomm_positions_long_all",
    "nc_short": "noncomm_positions_short_all",
    "c_long": "comm_positions_long_all",
    "c_short": "comm_positions_short_all",
}


def http_get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
    return raw.decode("utf-8", "replace")


def url(limit=160):
    q = {"cftc_contract_market_code": GOLD_CODE,
         "$order": f"{F['date']} DESC", "$limit": str(limit)}
    return DATASET + "?" + urllib.parse.urlencode(q)


def parse(text):
    rows = json.loads(text)
    if not rows:
        raise ValueError("CFTC returned no rows for gold")
    missing = [v for v in F.values() if v not in rows[0]]
    if missing:
        raise ValueError(f"CFTC fields changed; missing {missing}. Available: {sorted(rows[0])[:40]}")
    out = []
    for r in rows:
        nl, ns = float(r[F["nc_long"]]), float(r[F["nc_short"]])
        cl, cs = float(r[F["c_long"]]), float(r[F["c_short"]])
        oi = float(r[F["oi"]])
        out.append({"date": r[F["date"]][:10], "open_interest": int(oi),
                    "spec_long": int(nl), "spec_short": int(ns), "spec_net": int(nl - ns),
                    "comm_net": int(cl - cs),
                    "spec_net_pct_oi": round((nl - ns) / oi * 100, 1) if oi else None})
    out.sort(key=lambda x: x["date"])  # oldest first
    return out


def percentile(values, x):
    if not values:
        return None
    return round(sum(v <= x for v in values) / len(values) * 100)


def summarize(rows, weeks=6):
    last = rows[-1]
    prev = rows[-2] if len(rows) > 1 else None
    window = [r["spec_net"] for r in rows[-156:]]
    pct = percentile(window, last["spec_net"])
    if pct is None:
        crowd = ""
    elif pct >= 85:
        crowd = "crowded long: funds already hold a lot, less fuel for new buying and room for long liquidation"
    elif pct <= 15:
        crowd = "light positioning: funds hold little, room for them to buy"
    else:
        crowd = "middle of the 3-year range"
    return {
        "report_date": last["date"],
        "spec_net": last["spec_net"],
        "spec_net_change_week": last["spec_net"] - prev["spec_net"] if prev else None,
        "spec_net_pct_oi": last["spec_net_pct_oi"],
        "comm_net": last["comm_net"],
        "open_interest": last["open_interest"],
        "percentile_3y": pct,
        "reading": crowd,
        "history": rows[-weeks:],
        "note": "Positions as of Tuesday, published Friday. Positioning context, not a timing signal.",
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--weeks", type=int, default=6, help="weeks of history to show")
    ap.add_argument("--file", help="saved CFTC JSON instead of downloading")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    text = Path(a.file).read_text(encoding="utf-8") if a.file else http_get(url())
    s = summarize(parse(text), a.weeks)
    if a.json:
        print(json.dumps(s, indent=2))
        return
    ch = s["spec_net_change_week"]
    print(f"COMEX gold - CFTC COT, positions of {s['report_date']}")
    print(f"Funds (large specs) net long : {s['spec_net']:,} contracts"
          f" ({'n/a' if ch is None else f'{ch:+,}'} on the week), {s['spec_net_pct_oi']}% of open interest")
    print(f"Commercials net             : {s['comm_net']:,}")
    print(f"3-year percentile           : {s['percentile_3y']}  -> {s['reading']}")
    print("\nweek         spec net   change")
    prev = None
    for r in s["history"]:
        d = "" if prev is None else f"{r['spec_net'] - prev:+,}"
        print(f"{r['date']}  {r['spec_net']:>10,}  {d:>8}")
        prev = r["spec_net"]
    print("\n" + s["note"])


if __name__ == "__main__":
    main()
