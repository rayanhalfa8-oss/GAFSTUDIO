#!/usr/bin/env python3
"""Gold (XAUUSD) market clock: open/closed, active sessions, today's schedule.

Standard library only. Works without a timezone database: New York and London
daylight-saving rules are computed here, and the user's own timezone falls back
to the computer's local time if Python has no tz data (common on Windows).

    python3 sessions.py                 # now
    python3 sessions.py --at "2026-11-12 14:30"   # a local time
    python3 sessions.py --json
"""
import argparse
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

UTC = timezone.utc
DEFAULTS = {"timezone": "Africa/Casablanca"}


# ---------------------------------------------------------------- helpers
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


def _last_sunday(y, m, hour_utc):
    nxt = datetime(y + (m == 12), m % 12 + 1, 1, tzinfo=UTC)
    last = nxt - timedelta(days=1)
    return (last - timedelta(days=(last.weekday() - 6) % 7)).replace(hour=hour_utc)


def ny_offset(utc):
    """US DST: 2nd Sunday of March 02:00 local -> 1st Sunday of November 02:00."""
    start = _sunday_on_or_after(utc.year, 3, 8, 7)
    end = _sunday_on_or_after(utc.year, 11, 1, 6)
    return timedelta(hours=-4) if start <= utc < end else timedelta(hours=-5)


def london_offset(utc):
    """UK DST: last Sunday of March 01:00 UTC -> last Sunday of October 01:00 UTC."""
    start = _last_sunday(utc.year, 3, 1)
    end = _last_sunday(utc.year, 10, 1)
    return timedelta(hours=1) if start <= utc < end else timedelta(0)


def to_ny(utc):
    off = ny_offset(utc)
    return (utc + off).replace(tzinfo=timezone(off))


def to_london(utc):
    off = london_offset(utc)
    return (utc + off).replace(tzinfo=timezone(off))


# ---------------------------------------------------------------- market logic
def market_open(utc):
    """Spot gold trades Sun 18:00 -> Fri 17:00 New York, with a daily 17:00-18:00 break."""
    ny = to_ny(utc)
    wd, h = ny.weekday(), ny.hour  # Mon=0 .. Sun=6
    if wd == 5:
        return False, "weekend"
    if wd == 6:
        return (h >= 18), ("open" if h >= 18 else "weekend")
    if wd == 4 and h >= 17:
        return False, "weekend"
    if h == 17:
        return False, "daily break (17:00-18:00 New York)"
    return True, "open"


def active_sessions(utc):
    tokyo = utc + timedelta(hours=9)  # Japan has no DST
    lon, ny = to_london(utc), to_ny(utc)
    out = []
    if 9 <= tokyo.hour < 18 and tokyo.weekday() < 5:
        out.append("Asia (Tokyo)")
    if 8 <= lon.hour < 17 and lon.weekday() < 5:
        out.append("London")
    if 8 <= ny.hour < 17 and ny.weekday() < 5:
        out.append("New York")
    return out


def session_label(utc):
    s = active_sessions(utc)
    if "London" in s and "New York" in s:
        return "London+NY overlap"
    return s[0] if s else "Off-hours"


def schedule_for_day(day_local, tz):
    """Each session's open/close for a local calendar date, in local time."""
    noon_utc = datetime(day_local.year, day_local.month, day_local.day, 12, tzinfo=tz).astimezone(UTC)
    d = noon_utc.date()
    rows = []
    tok_open = datetime(d.year, d.month, d.day, 0, tzinfo=UTC)  # 09:00 JST
    rows.append(("Asia (Tokyo)", tok_open, tok_open + timedelta(hours=9)))
    lo = london_offset(noon_utc)
    lon_open = datetime(d.year, d.month, d.day, 8, tzinfo=UTC) - lo
    rows.append(("London", lon_open, lon_open + timedelta(hours=9)))
    no = ny_offset(noon_utc)
    ny_open = datetime(d.year, d.month, d.day, 8, tzinfo=UTC) - no
    rows.append(("New York", ny_open, ny_open + timedelta(hours=9)))
    rows.append(("London+NY overlap", ny_open, lon_open + timedelta(hours=9)))
    return [(n, a.astimezone(tz), b.astimezone(tz)) for n, a, b in rows]


def status(utc, tz):
    is_open, why = market_open(utc)
    local = utc.astimezone(tz)
    return {
        "local_time": local.strftime("%Y-%m-%d %H:%M %a"),
        "new_york_time": to_ny(utc).strftime("%H:%M"),
        "london_time": to_london(utc).strftime("%H:%M"),
        "market_open": is_open,
        "market_state": why,
        "active_sessions": active_sessions(utc) if is_open else [],
        "session": session_label(utc) if is_open else "Closed",
        "schedule_local": [
            {"session": n, "open": a.strftime("%H:%M"), "close": b.strftime("%H:%M")}
            for n, a, b in schedule_for_day(local.date(), tz)
        ],
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--at", help='local time "YYYY-MM-DD HH:MM" instead of now')
    ap.add_argument("--tz", help="IANA timezone, e.g. Africa/Casablanca (default from gold/config.json)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    tz = local_tz(a.tz or load_config()["timezone"])
    if a.at:
        utc = datetime.strptime(a.at, "%Y-%m-%d %H:%M").replace(tzinfo=tz).astimezone(UTC)
    else:
        utc = datetime.now(UTC)
    st = status(utc, tz)
    if a.json:
        print(json.dumps(st, indent=2, ensure_ascii=False))
        return
    print(f"Local time : {st['local_time']}   (New York {st['new_york_time']}, London {st['london_time']})")
    print(f"Market     : {'OPEN' if st['market_open'] else 'CLOSED'} - {st['market_state']}")
    print(f"Session    : {st['session']}")
    print("\nToday's sessions (your local time):")
    for r in st["schedule_local"]:
        print(f"  {r['session']:<20} {r['open']} -> {r['close']}")
    print("\nNote: bank holidays (US/UK) are not included; liquidity is thin on those days.")


if __name__ == "__main__":
    main()
