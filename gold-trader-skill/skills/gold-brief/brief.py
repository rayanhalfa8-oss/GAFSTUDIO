#!/usr/bin/env python3
"""Daily gold brief: gathers everything the other gold skills know, in one JSON.

It runs the sibling tools (sessions, econ, macro, cot, news) and saves the raw
facts to gold/brief-YYYY-MM-DD.json. Claude then writes the human brief from
it, in the user's language. A part that fails (no network, site changed) is
reported as unavailable instead of stopping the whole brief.

    python3 brief.py                 # print JSON and save it
    python3 brief.py --skip cot news
"""
import argparse
import importlib.util
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

UTC = timezone.utc
HERE = Path(__file__).resolve().parent
PARTS = {
    "sessions": ("gold-sessions", "sessions.py"),
    "econ": ("gold-econ", "econ.py"),
    "macro": ("gold-macro", "macro.py"),
    "cot": ("gold-cot", "cot.py"),
    "news": ("gold-news", "news.py"),
}


def load(name):
    folder, file = PARTS[name]
    path = HERE.parent / folder / file
    spec = importlib.util.spec_from_file_location(f"gold_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_part(name, now):
    m = load(name)
    if name == "sessions":
        return m.status(now, m.local_tz(m.load_config()["timezone"]))
    if name == "econ":
        cfg = m.load_config()
        events = m.parse_events(m.fetch_feed("this"), ("USD",), "high")
        m.write_cache(events, int(cfg["news_blackout_minutes"]))
        medium = m.parse_events(m.fetch_feed("this"), ("USD",), "medium")
        return {"high_impact_usd_this_week": events,
                "medium_and_high_count": len(medium),
                "timezone": cfg["timezone"], "blackout_minutes": cfg["news_blackout_minutes"]}
    if name == "macro":
        data, errors = m.fetch_all()
        out = m.build(data)
        out["errors"] = errors
        return out
    if name == "cot":
        s = m.summarize(m.parse(m.http_get(m.url())))
        s["history"] = s["history"][-4:]
        return s
    if name == "news":
        texts = []
        for q in m.DEFAULT_QUERIES:
            try:
                texts.append(m.http_get(m.rss_url(q, 24)))
            except Exception:
                pass
        if not texts:
            raise RuntimeError("no news feed reachable")
        return m.collect(texts, 24)[:20]
    raise KeyError(name)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skip", nargs="*", default=[], choices=list(PARTS))
    a = ap.parse_args(argv)
    now = datetime.now(UTC)
    brief = {"generated_utc": now.isoformat(timespec="minutes"), "unavailable": {}}
    for name in PARTS:
        if name in a.skip:
            continue
        try:
            brief[name] = run_part(name, now)
        except Exception as e:  # keep going: a partial brief beats none
            brief["unavailable"][name] = f"{type(e).__name__}: {e}"
    d = Path(os.environ.get("GOLD_DIR", "gold"))
    d.mkdir(parents=True, exist_ok=True)
    out = d / f"brief-{now.strftime('%Y-%m-%d')}.json"
    out.write_text(json.dumps(brief, indent=2, ensure_ascii=False), encoding="utf-8")
    json.dump(brief, sys.stdout, indent=2, ensure_ascii=False)
    print(f"\n\nsaved: {out}")


if __name__ == "__main__":
    main()
