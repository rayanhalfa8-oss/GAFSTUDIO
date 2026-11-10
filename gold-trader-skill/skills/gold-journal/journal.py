#!/usr/bin/env python3
"""XAUUSD trading journal and statistics (gold/journal.csv).

Logs each trade and measures the strategy with numbers, not feelings:
win rate, average win vs loss, profit factor, expectancy (in $ and in R),
longest losing streak, max drawdown, and results by session, weekday and setup.
It never judges the strategy's rules: it only counts what happened.

    python3 journal.py add --side buy --entry 2650 --sl 2645 --exit 2660 --lots 0.2 \
        --open "2026-11-10 10:15" --setup "my setup A" --pnl 198.4
    python3 journal.py list --last 10
    python3 journal.py stats
    python3 journal.py stats --from 2026-11-01 --setup "my setup A"
    python3 journal.py today                  # trades and P/L today (used by /gold-risk)
"""
import argparse
import csv
import json
import os
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

UTC = timezone.utc
DEFAULTS = {"timezone": "Africa/Casablanca", "contract_size": 100}
COLS = ["id", "open_time", "close_time", "side", "entry", "sl", "tp", "exit", "lots",
        "pnl", "r", "session", "setup", "notes"]


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


def _sunday_on_or_after(y, m, d, hour_utc):
    base = datetime(y, m, d, tzinfo=UTC)
    return (base + timedelta(days=(6 - base.weekday()) % 7)).replace(hour=hour_utc)


def _last_sunday(y, m, hour_utc):
    nxt = datetime(y + (m == 12), m % 12 + 1, 1, tzinfo=UTC)
    last = nxt - timedelta(days=1)
    return (last - timedelta(days=(last.weekday() - 6) % 7)).replace(hour=hour_utc)


def session_of(utc):
    ny_off = timedelta(hours=-4) if _sunday_on_or_after(utc.year, 3, 8, 7) <= utc < _sunday_on_or_after(utc.year, 11, 1, 6) else timedelta(hours=-5)
    lon_off = timedelta(hours=1) if _last_sunday(utc.year, 3, 1) <= utc < _last_sunday(utc.year, 10, 1) else timedelta(0)
    lon, ny, tok = (utc + lon_off).hour, (utc + ny_off).hour, (utc + timedelta(hours=9)).hour
    in_lon, in_ny = 8 <= lon < 17, 8 <= ny < 17
    if in_lon and in_ny:
        return "London+NY overlap"
    if in_lon:
        return "London"
    if in_ny:
        return "New York"
    if 9 <= tok < 18:
        return "Asia"
    return "Off-hours"


def journal_path():
    return data_dir() / "journal.csv"


def read_trades():
    p = journal_path()
    if not p.exists():
        return []
    with p.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_trades(rows):
    with journal_path().open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in COLS})


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------- stats
def stats(trades):
    pnls = [num(t["pnl"]) for t in trades if num(t["pnl"]) is not None]
    rs = [num(t["r"]) for t in trades if num(t.get("r")) is not None]
    if not pnls:
        return {"trades": 0}
    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p < 0]
    eq, peak, mdd = 0.0, 0.0, 0.0
    streak = worst = 0
    for p in pnls:
        eq += p
        peak = max(peak, eq)
        mdd = max(mdd, peak - eq)
        streak = streak + 1 if p < 0 else 0
        worst = max(worst, streak)
    gross_win, gross_loss = sum(wins), -sum(losses)
    return {
        "trades": len(pnls),
        "wins": len(wins), "losses": len(losses), "breakeven": len(pnls) - len(wins) - len(losses),
        "win_rate": round(len(wins) / len(pnls) * 100, 1),
        "net_pnl": round(sum(pnls), 2),
        "avg_win": round(gross_win / len(wins), 2) if wins else 0,
        "avg_loss": round(-gross_loss / len(losses), 2) if losses else 0,
        "profit_factor": round(gross_win / gross_loss, 2) if gross_loss else None,
        "expectancy_per_trade": round(sum(pnls) / len(pnls), 2),
        "avg_r": round(sum(rs) / len(rs), 2) if rs else None,
        "max_losing_streak": worst,
        "max_drawdown": round(mdd, 2),
        "best": round(max(pnls), 2), "worst": round(min(pnls), 2),
    }


def by(trades, key):
    groups = defaultdict(list)
    for t in trades:
        groups[key(t) or "-"].append(t)
    return {k: stats(v) for k, v in sorted(groups.items())}


def weekday(t):
    try:
        return datetime.fromisoformat(t["open_time"]).strftime("%a")
    except ValueError:
        return "-"


def today_summary(trades, tz, now=None):
    now = now or datetime.now(UTC)
    d = now.astimezone(tz).date()
    todays = []
    for t in trades:
        try:
            if datetime.fromisoformat(t["open_time"]).astimezone(tz).date() == d:
                todays.append(t)
        except ValueError:
            pass
    pnl = sum(num(t["pnl"]) or 0 for t in todays)
    return {"date": d.isoformat(), "trades": len(todays), "pnl": round(pnl, 2)}


# ---------------------------------------------------------------- commands
def cmd_add(a, cfg, tz):
    side = a.side.upper()
    sign = 1 if side == "BUY" else -1
    opened = datetime.strptime(a.open, "%Y-%m-%d %H:%M").replace(tzinfo=tz) if a.open else datetime.now(tz)
    closed = datetime.strptime(a.close, "%Y-%m-%d %H:%M").replace(tzinfo=tz) if a.close else None
    pnl = a.pnl
    if pnl is None and a.exit is not None:
        pnl = round((a.exit - a.entry) * sign * a.lots * cfg["contract_size"], 2)
    r = None
    if a.exit is not None and a.sl is not None and a.sl != a.entry:
        r = round((a.exit - a.entry) * sign / abs(a.entry - a.sl), 2)
    rows = read_trades()
    nid = max([int(x["id"]) for x in rows if x["id"].isdigit()] + [0]) + 1
    row = {"id": nid, "open_time": opened.isoformat(timespec="minutes"),
           "close_time": closed.isoformat(timespec="minutes") if closed else "",
           "side": side, "entry": a.entry, "sl": a.sl if a.sl is not None else "", "tp": a.tp if a.tp is not None else "",
           "exit": a.exit if a.exit is not None else "", "lots": a.lots,
           "pnl": pnl if pnl is not None else "", "r": r if r is not None else "",
           "session": session_of(opened.astimezone(UTC)), "setup": a.setup or "", "notes": a.notes or ""}
    rows.append(row)
    write_trades(rows)
    print(f"Saved trade #{nid}: {side} {a.lots} @ {a.entry}  P/L {row['pnl']}  R {row['r']}  ({row['session']})")


def filtered(a):
    rows = read_trades()
    if a.frm:
        rows = [t for t in rows if t["open_time"][:10] >= a.frm]
    if a.to:
        rows = [t for t in rows if t["open_time"][:10] <= a.to]
    if a.setup:
        rows = [t for t in rows if t["setup"] == a.setup]
    return rows


def print_stats(s, label="ALL"):
    if not s.get("trades"):
        print(f"{label}: no closed trades")
        return
    pf = s["profit_factor"] if s["profit_factor"] is not None else "inf"
    print(f"{label}: {s['trades']} trades | win {s['win_rate']}% | net {s['net_pnl']}$ | "
          f"avg win {s['avg_win']}$ / avg loss {s['avg_loss']}$ | PF {pf} | "
          f"exp {s['expectancy_per_trade']}$/trade | avg R {s['avg_r']} | "
          f"worst streak {s['max_losing_streak']} | max DD {s['max_drawdown']}$")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("add")
    p.add_argument("--side", required=True, choices=["buy", "sell"])
    p.add_argument("--entry", type=float, required=True)
    p.add_argument("--sl", type=float)
    p.add_argument("--tp", type=float)
    p.add_argument("--exit", type=float)
    p.add_argument("--lots", type=float, required=True)
    p.add_argument("--pnl", type=float, help="real P/L from the broker (includes swap/commission); preferred")
    p.add_argument("--open", help='"YYYY-MM-DD HH:MM" local time (default now)')
    p.add_argument("--close", help='"YYYY-MM-DD HH:MM" local time')
    p.add_argument("--setup", help="your own name for the setup")
    p.add_argument("--notes")
    for name in ("list", "stats"):
        q = sub.add_parser(name)
        q.add_argument("--from", dest="frm", help="YYYY-MM-DD")
        q.add_argument("--to", help="YYYY-MM-DD")
        q.add_argument("--setup")
        q.add_argument("--json", action="store_true")
        if name == "list":
            q.add_argument("--last", type=int, default=20)
    t = sub.add_parser("today")
    t.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    cfg = load_config()
    tz = local_tz(cfg["timezone"])
    if a.cmd == "add":
        cmd_add(a, cfg, tz)
    elif a.cmd == "today":
        s = today_summary(read_trades(), tz)
        print(json.dumps(s) if a.json else f"Today {s['date']}: {s['trades']} trade(s), P/L {s['pnl']}$")
    elif a.cmd == "list":
        rows = filtered(a)[-a.last:]
        if a.json:
            print(json.dumps(rows, indent=2))
            return
        for r in rows:
            print(f"#{r['id']:>3} {r['open_time']}  {r['side']:<4} {r['lots']:>5} @ {r['entry']:<8} "
                  f"exit {r['exit']:<8} P/L {r['pnl']:>8}  R {r['r']:>5}  {r['session']:<17} {r['setup']}")
    else:
        rows = filtered(a)
        out = {"all": stats(rows), "by_session": by(rows, lambda t: t["session"]),
               "by_weekday": by(rows, weekday), "by_setup": by(rows, lambda t: t["setup"])}
        if a.json:
            print(json.dumps(out, indent=2))
            return
        print_stats(out["all"])
        for title in ("by_session", "by_weekday", "by_setup"):
            print(f"\n{title.replace('_', ' ')}:")
            for k, s in out[title].items():
                print_stats(s, "  " + k)
        n = out["all"].get("trades", 0)
        if n and n < 30:
            print(f"\nOnly {n} trades: too few to judge the strategy. Aim for 30-50+ before drawing conclusions.")


if __name__ == "__main__":
    main()
