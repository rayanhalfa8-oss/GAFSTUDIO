#!/usr/bin/env python3
"""Pre-trade risk check for XAUUSD: PASS / WARN / BLOCK against YOUR limits.

It does not judge the setup or the strategy. It only checks the trade against
the money and timing rules you set in gold/config.json:
  - risk at stop <= max risk % of balance
  - reward:risk >= your minimum (when a take-profit is given)
  - trades today < your daily maximum            (reads gold/journal.csv)
  - today's loss has not hit your daily limit     (reads gold/journal.csv)
  - no high-impact USD news within the blackout   (reads gold/calendar.json from /gold-econ)
  - spread <= your maximum (when given)
  - the market is open

    python3 check.py --entry 2650 --sl 2645 --lots 0.2 --tp 2660 --spread 0.3
    python3 check.py --entry 2650 --sl 2645 --lots 0.2 --at "2026-11-12 14:20"
"""
import argparse
import csv
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

UTC = timezone.utc
DEFAULTS = {"timezone": "Africa/Casablanca", "account_balance": 1000, "contract_size": 100,
            "max_risk_percent": 1.0, "min_rr": 1.5, "max_trades_per_day": 3,
            "max_daily_loss_percent": 3.0, "news_blackout_minutes": 15, "max_spread": 0.5}


def data_dir():
    return Path(os.environ.get("GOLD_DIR", "gold"))


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


def _sunday_on_or_after(y, m, d, hour_utc):
    base = datetime(y, m, d, tzinfo=UTC)
    return (base + timedelta(days=(6 - base.weekday()) % 7)).replace(hour=hour_utc)


def market_open(utc):
    off = timedelta(hours=-4) if _sunday_on_or_after(utc.year, 3, 8, 7) <= utc < _sunday_on_or_after(utc.year, 11, 1, 6) else timedelta(hours=-5)
    ny = utc + off
    wd, h = ny.weekday(), ny.hour
    if wd == 5 or (wd == 6 and h < 18) or (wd == 4 and h >= 17):
        return False, "weekend"
    if h == 17:
        return False, "daily break 17:00-18:00 New York"
    return True, "open"


def today_from_journal(tz, now):
    p = data_dir() / "journal.csv"
    if not p.exists():
        return 0, 0.0, False
    d = now.astimezone(tz).date()
    n, pnl = 0, 0.0
    with p.open(encoding="utf-8", newline="") as f:
        for t in csv.DictReader(f):
            try:
                if datetime.fromisoformat(t["open_time"]).astimezone(tz).date() != d:
                    continue
            except ValueError:
                continue
            n += 1
            try:
                pnl += float(t["pnl"])
            except (TypeError, ValueError):
                pass
    return n, pnl, True


def news_near(now, blackout):
    p = data_dir() / "calendar.json"
    if not p.exists():
        return None, []
    cal = json.loads(p.read_text(encoding="utf-8"))
    near = []
    for e in cal.get("events", []):
        if e.get("impact") != "High":
            continue
        t = datetime.fromisoformat(e["time_utc"])
        mins = (t - now).total_seconds() / 60
        if -blackout <= mins <= blackout:
            near.append((e, round(mins)))
    return cal.get("updated_utc"), near


def check(cfg, entry, sl, lots, tp=None, spread=None, now=None, tz=UTC):
    now = now or datetime.now(UTC)
    res = []

    def add(level, rule, msg):
        res.append({"level": level, "rule": rule, "detail": msg})

    bal = float(cfg["account_balance"])
    risk = abs(entry - sl) * lots * cfg["contract_size"]
    rp = risk / bal * 100 if bal else 0
    add("PASS" if rp <= cfg["max_risk_percent"] + 1e-9 else "BLOCK", "risk per trade",
        f"{risk:.2f}$ at stop = {rp:.2f}% of {bal:.0f}$ (limit {cfg['max_risk_percent']}%)")

    if tp is not None:
        side_ok = (tp > entry) == (sl < entry)
        if not side_ok:
            add("BLOCK", "take-profit", "take-profit is on the same side as the stop")
        else:
            rr = abs(tp - entry) / abs(entry - sl)
            add("PASS" if rr >= cfg["min_rr"] else "WARN", "reward:risk", f"1:{rr:.2f} (your minimum 1:{cfg['min_rr']})")
    else:
        add("WARN", "take-profit", "no take-profit given, R:R not checked")

    n, pnl, has_journal = today_from_journal(tz, now)
    if has_journal:
        add("PASS" if n < cfg["max_trades_per_day"] else "BLOCK", "trades today",
            f"{n} already today (limit {cfg['max_trades_per_day']})")
        limit = bal * cfg["max_daily_loss_percent"] / 100
        add("PASS" if pnl > -limit else "BLOCK", "daily loss",
            f"today's P/L {pnl:.2f}$ (stop trading at -{limit:.2f}$)")
    else:
        add("WARN", "journal", "no gold/journal.csv: daily trade count and loss limit not checked")

    updated, near = news_near(now, cfg["news_blackout_minutes"])
    if updated is None:
        add("WARN", "news", "no gold/calendar.json: run /gold-econ first to check news times")
    elif near:
        for e, mins in near:
            when = f"in {mins} min" if mins >= 0 else f"{-mins} min ago"
            add("BLOCK", "news blackout", f"{e['currency']} {e['title']} {when} (blackout +/-{cfg['news_blackout_minutes']} min)")
    else:
        try:
            age_h = (now - datetime.fromisoformat(updated)).total_seconds() / 3600
        except ValueError:
            age_h = 0
        stale = f" (calendar is {age_h:.0f}h old, refresh with /gold-econ)" if age_h > 24 else ""
        add("PASS" if not stale else "WARN", "news", "no high-impact USD news inside the blackout" + stale)

    if spread is not None:
        add("PASS" if spread <= cfg["max_spread"] else "BLOCK", "spread", f"{spread} (limit {cfg['max_spread']})")

    ok, why = market_open(now)
    add("PASS" if ok else "BLOCK", "market", why)

    levels = [r["level"] for r in res]
    verdict = "BLOCK" if "BLOCK" in levels else ("WARN" if "WARN" in levels else "PASS")
    return {"verdict": verdict, "checks": res}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--entry", type=float, required=True)
    ap.add_argument("--sl", type=float, required=True)
    ap.add_argument("--lots", type=float, required=True)
    ap.add_argument("--tp", type=float)
    ap.add_argument("--spread", type=float, help="current spread in $ (e.g. 0.30)")
    ap.add_argument("--at", help='local time "YYYY-MM-DD HH:MM" instead of now')
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    cfg = load_config()
    tz = local_tz(cfg["timezone"])
    now = datetime.strptime(a.at, "%Y-%m-%d %H:%M").replace(tzinfo=tz).astimezone(UTC) if a.at else datetime.now(UTC)
    r = check(cfg, a.entry, a.sl, a.lots, a.tp, a.spread, now, tz)
    if a.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
        return
    for c in r["checks"]:
        print(f"[{c['level']:<5}] {c['rule']:<15} {c['detail']}")
    print(f"\nVERDICT: {r['verdict']}")


if __name__ == "__main__":
    main()
