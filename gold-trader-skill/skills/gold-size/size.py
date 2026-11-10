#!/usr/bin/env python3
"""XAUUSD position size calculator: how many lots for the risk you chose.

Works from your entry and stop-loss prices (your strategy decides those; this
only does the arithmetic). 1 standard lot = 100 oz by default, so a 1$ move in
gold = 100$ per lot. Check your broker's contract size and set it in
gold/config.json if it differs.

    python3 size.py --entry 2650.50 --sl 2645.50                 # uses config balance/risk
    python3 size.py --balance 1000 --risk 1 --entry 2650 --sl 2656 --tp 2638
    python3 size.py --balance 1000 --risk-money 15 --entry 2650 --sl-distance 4
"""
import argparse
import json
import math
import os
from pathlib import Path

DEFAULTS = {"account_balance": 1000, "risk_percent": 1.0, "contract_size": 100,
            "min_lot": 0.01, "lot_step": 0.01, "max_lot": 100, "leverage": 100}


def data_dir():
    return Path(os.environ.get("GOLD_DIR", "gold"))


def load_config():
    cfg = dict(DEFAULTS)
    p = data_dir() / "config.json"
    if p.exists():
        cfg.update(json.loads(p.read_text(encoding="utf-8")))
    return cfg


def floor_step(x, step):
    return math.floor(x / step + 1e-9) * step


def compute(balance, entry, sl, risk_percent=None, risk_money=None, tp=None,
            contract_size=100, min_lot=0.01, lot_step=0.01, max_lot=100, leverage=100):
    if entry <= 0 or sl <= 0:
        raise ValueError("entry and stop-loss must be prices above 0")
    dist = abs(entry - sl)
    if dist == 0:
        raise ValueError("stop-loss cannot equal entry")
    side = "BUY" if sl < entry else "SELL"
    if tp is not None and ((side == "BUY" and tp <= entry) or (side == "SELL" and tp >= entry)):
        raise ValueError(f"take-profit {tp} is on the wrong side of entry for a {side}")
    budget = risk_money if risk_money is not None else balance * (risk_percent or 0) / 100
    if budget <= 0:
        raise ValueError("risk must be above 0")
    loss_per_lot = dist * contract_size
    raw = budget / loss_per_lot
    lots = min(floor_step(raw, lot_step), max_lot)
    warnings = []
    if lots < min_lot:
        lots = min_lot
        warnings.append(f"Even the minimum lot ({min_lot}) risks {min_lot * loss_per_lot:.2f}$, "
                        f"more than your {budget:.2f}$. Skip the trade, or take it knowing the risk is bigger.")
    lots = round(lots, 4)
    real_risk = lots * loss_per_lot
    sign = 1 if side == "BUY" else -1
    targets = {f"{r}R": round(entry + sign * dist * r, 2) for r in (1, 1.5, 2, 3)}
    out = {
        "side": side, "entry": entry, "stop_loss": sl,
        "stop_distance_usd": round(dist, 2), "stop_distance_points": round(dist * 100),
        "risk_budget": round(budget, 2), "lots": lots,
        "risk_at_stop": round(real_risk, 2),
        "risk_percent_of_balance": round(real_risk / balance * 100, 2) if balance else None,
        "value_per_1usd_move": round(lots * contract_size, 2),
        "margin_estimate": round(lots * contract_size * entry / leverage, 2),
        "targets": targets, "warnings": warnings,
    }
    if tp is not None:
        reward = abs(tp - entry)
        out["take_profit"] = tp
        out["reward_at_tp"] = round(lots * reward * contract_size, 2)
        out["rr"] = round(reward / dist, 2)
    if balance and out["margin_estimate"] > balance:
        warnings.append("Estimated margin is above your balance: the broker may refuse the order.")
    return out


def main(argv=None):
    cfg = load_config()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--balance", type=float, default=cfg["account_balance"])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--risk", type=float, help="risk in percent of balance (default from config)")
    g.add_argument("--risk-money", type=float, help="risk in dollars")
    ap.add_argument("--entry", type=float, required=True)
    s = ap.add_mutually_exclusive_group(required=True)
    s.add_argument("--sl", type=float, help="stop-loss price")
    s.add_argument("--sl-distance", type=float, help="stop distance in $ (e.g. 5 = 500 points); needs --side")
    ap.add_argument("--side", choices=["buy", "sell"], help="with --sl-distance")
    ap.add_argument("--tp", type=float)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    sl = a.sl
    if sl is None:
        if not a.side:
            ap.error("--sl-distance needs --side buy|sell")
        sl = a.entry - a.sl_distance if a.side == "buy" else a.entry + a.sl_distance
    risk_pct = a.risk if a.risk is not None else (None if a.risk_money is not None else cfg["risk_percent"])
    try:
        r = compute(a.balance, a.entry, sl, risk_pct, a.risk_money, a.tp,
                    cfg["contract_size"], cfg["min_lot"], cfg["lot_step"], cfg["max_lot"], cfg["leverage"])
    except ValueError as e:
        raise SystemExit(f"error: {e}")
    if a.json:
        print(json.dumps(r, indent=2))
        return
    print(f"{r['side']} XAUUSD  entry {r['entry']}  stop {r['stop_loss']}  "
          f"(distance {r['stop_distance_usd']}$ = {r['stop_distance_points']} points)")
    print(f"Risk budget : {r['risk_budget']}$")
    print(f"LOT SIZE    : {r['lots']}")
    print(f"Loss at stop: {r['risk_at_stop']}$ ({r['risk_percent_of_balance']}% of balance)")
    print(f"Each 1$ move in gold = {r['value_per_1usd_move']}$ for you")
    print(f"Margin (est., 1:{cfg['leverage']}): {r['margin_estimate']}$")
    if "take_profit" in r:
        print(f"Take-profit {r['take_profit']}: +{r['reward_at_tp']}$  (R:R = 1:{r['rr']})")
    print("Targets by R: " + "  ".join(f"{k} {v}" for k, v in r["targets"].items()))
    for w in r["warnings"]:
        print(f"WARNING: {w}")


if __name__ == "__main__":
    main()
