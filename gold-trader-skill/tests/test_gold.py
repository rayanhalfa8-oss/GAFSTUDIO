"""Offline tests for the gold skills. Run: python3 -m unittest discover -s tests -v"""
import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "skills"
FX = Path(__file__).resolve().parent / "fixtures"
UTC = timezone.utc


def load(folder, file):
    spec = importlib.util.spec_from_file_location(file[:-3] + "_t", ROOT / folder / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


sessions = load("gold-sessions", "sessions.py")
econ = load("gold-econ", "econ.py")
news = load("gold-news", "news.py")
macro = load("gold-macro", "macro.py")
cot = load("gold-cot", "cot.py")
size = load("gold-size", "size.py")
journal = load("gold-journal", "journal.py")
check = load("gold-risk", "check.py")


class TmpDir(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        os.environ["GOLD_DIR"] = self.d

    def tearDown(self):
        shutil.rmtree(self.d)
        os.environ.pop("GOLD_DIR", None)


class Sessions(unittest.TestCase):
    def test_dst_offsets(self):
        self.assertEqual(sessions.ny_offset(datetime(2026, 7, 1, 12, tzinfo=UTC)).total_seconds(), -4 * 3600)
        self.assertEqual(sessions.ny_offset(datetime(2026, 11, 10, 12, tzinfo=UTC)).total_seconds(), -5 * 3600)
        # US DST 2026 ends Sunday 1 Nov at 06:00 UTC
        self.assertEqual(sessions.ny_offset(datetime(2026, 11, 1, 5, 59, tzinfo=UTC)).total_seconds(), -4 * 3600)
        self.assertEqual(sessions.ny_offset(datetime(2026, 11, 1, 6, 0, tzinfo=UTC)).total_seconds(), -5 * 3600)
        # UK DST 2026: 29 Mar -> 25 Oct
        self.assertEqual(sessions.london_offset(datetime(2026, 3, 29, 1, tzinfo=UTC)).total_seconds(), 3600)
        self.assertEqual(sessions.london_offset(datetime(2026, 10, 25, 1, tzinfo=UTC)).total_seconds(), 0)

    def test_market_hours(self):
        sat = datetime(2026, 11, 14, 12, tzinfo=UTC)
        self.assertFalse(sessions.market_open(sat)[0])
        self.assertFalse(sessions.market_open(datetime(2026, 11, 13, 22, 30, tzinfo=UTC))[0])  # Fri 17:30 NY
        self.assertTrue(sessions.market_open(datetime(2026, 11, 15, 23, 30, tzinfo=UTC))[0])   # Sun 18:30 NY
        self.assertFalse(sessions.market_open(datetime(2026, 11, 10, 22, 30, tzinfo=UTC))[0])  # daily break
        self.assertTrue(sessions.market_open(datetime(2026, 11, 10, 15, tzinfo=UTC))[0])

    def test_sessions(self):
        self.assertEqual(sessions.session_label(datetime(2026, 11, 10, 14, tzinfo=UTC)), "London+NY overlap")
        self.assertEqual(sessions.session_label(datetime(2026, 11, 10, 9, tzinfo=UTC)), "London")
        self.assertEqual(sessions.session_label(datetime(2026, 11, 10, 2, tzinfo=UTC)), "Asia (Tokyo)")
        self.assertEqual(journal.session_of(datetime(2026, 11, 10, 14, tzinfo=UTC)), "London+NY overlap")
        self.assertEqual(journal.session_of(datetime(2026, 11, 10, 19, tzinfo=UTC)), "New York")


class Econ(TmpDir):
    def test_parse_and_tags(self):
        text = (FX / "ff_week.json").read_text()
        ev = econ.parse_events(text, ("USD",), "High")
        self.assertEqual([e["title"] for e in ev], ["CPI m/m", "Core CPI m/m", "Fed Chair Powell Speaks"])
        self.assertEqual(ev[0]["time_utc"], "2026-11-12T13:30:00+00:00")
        self.assertEqual(ev[0]["tag"], "Inflation")
        self.assertEqual(ev[2]["tag"], "Fed")
        med = econ.parse_events(text, ("USD",), "Medium")
        self.assertIn("Jobs", [e["tag"] for e in med])
        self.assertEqual(len(econ.parse_events(text, (), "Medium")), 5)  # holiday dropped, EUR kept

    def test_cache(self):
        ev = econ.parse_events((FX / "ff_week.json").read_text())
        p = econ.write_cache(ev, 15)
        self.assertEqual(json.loads(p.read_text())["blackout_minutes"], 15)


class News(TmpDir):
    def test_parse_dedupe_tags(self):
        text = (FX / "news.xml").read_text()
        items = news.collect([text], 24, now=datetime(2026, 11, 10, 12, tzinfo=UTC))
        self.assertEqual(len(items), 2)  # duplicate merged, old story dropped
        self.assertEqual(items[0]["title"], "Gold hits record as dollar slips")
        self.assertIn("Dollar", items[0]["tags"])
        self.assertIn("Fed", items[1]["tags"])
        self.assertNotIn("Geopolitics", news.tags_for("Old story about warnings"))

    def test_only_new(self):
        items = news.collect([(FX / "news.xml").read_text()], 24, now=datetime(2026, 11, 10, 12, tzinfo=UTC))
        self.assertEqual(len(news.only_new(items)), 2)
        self.assertEqual(len(news.only_new(items)), 0)


class Macro(unittest.TestCase):
    def test_build(self):
        g = macro.parse_yahoo((FX / "yahoo_gold.json").read_text())
        d = macro.parse_yahoo((FX / "yahoo_dxy.json").read_text())
        r = macro.parse_fred((FX / "fred_dfii10.csv").read_text())
        self.assertEqual(len(g), 69)  # one None dropped
        self.assertEqual([x[1] for x in r], [1.90, 1.85, 1.84, 1.80, 1.78, 1.75])
        out = macro.build({"GC=F": g, "DX-Y.NYB": d, "DFII10": r})
        rows = {x["symbol"]: x for x in out["drivers"]}
        self.assertEqual(rows["DX-Y.NYB"]["for_gold"], "neutral")   # -0.1% in 5d < 0.3 threshold
        self.assertEqual(rows["DFII10"]["chg_5d"], -15.0)
        self.assertEqual(rows["DFII10"]["for_gold"], "TAILWIND")
        self.assertEqual(rows["^TNX"].get("error"), "no data")
        self.assertLess(out["corr_60d_with_gold"]["DX-Y.NYB"], 0)


class Cot(unittest.TestCase):
    def test_summary(self):
        rows = cot.parse((FX / "cot_gold.json").read_text())
        self.assertEqual(rows[-1]["date"], "2026-11-04")
        s = cot.summarize(rows)
        self.assertEqual(s["spec_net"], 200000 + 160 * 500 - 50000)
        self.assertEqual(s["spec_net_change_week"], 500)
        self.assertEqual(s["percentile_3y"], 100)
        self.assertIn("crowded", s["reading"])
        self.assertEqual(s["comm_net"], -190000)

    def test_changed_fields(self):
        with self.assertRaises(ValueError):
            cot.parse(json.dumps([{"report_date_as_yyyy_mm_dd": "2026-11-04"}]))


class Size(unittest.TestCase):
    def test_buy(self):
        r = size.compute(10000, 2650, 2645, risk_percent=1)
        self.assertEqual(r["side"], "BUY")
        self.assertEqual(r["lots"], 0.2)
        self.assertEqual(r["risk_at_stop"], 100.0)
        self.assertEqual(r["stop_distance_points"], 500)
        self.assertEqual(r["targets"]["2R"], 2660)

    def test_sell_rounding_and_tp(self):
        r = size.compute(1000, 2650, 2656.5, risk_percent=1, tp=2637)
        self.assertEqual(r["side"], "SELL")
        self.assertEqual(r["lots"], 0.01)          # 10$/650$ = 0.015 -> floored to 0.01
        self.assertEqual(r["risk_at_stop"], 6.5)
        self.assertEqual(r["rr"], 2.0)

    def test_too_small(self):
        r = size.compute(100, 2650, 2630, risk_percent=1)
        self.assertEqual(r["lots"], 0.01)
        self.assertTrue(r["warnings"])

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            size.compute(1000, 2650, 2650, risk_percent=1)
        with self.assertRaises(ValueError):
            size.compute(1000, 2650, 2645, risk_percent=1, tp=2640)


class Journal(TmpDir):
    def add(self, *args):
        journal.main(["add"] + list(args))

    def test_stats(self):
        self.add("--side", "buy", "--entry", "2650", "--sl", "2645", "--exit", "2660", "--lots", "0.1", "--open", "2026-11-09 10:00")
        self.add("--side", "sell", "--entry", "2660", "--sl", "2665", "--exit", "2665", "--lots", "0.1", "--open", "2026-11-09 15:00")
        self.add("--side", "sell", "--entry", "2660", "--sl", "2665", "--exit", "2665", "--lots", "0.1", "--pnl", "-52", "--open", "2026-11-10 15:00")
        rows = journal.read_trades()
        self.assertEqual(rows[0]["pnl"], "100.0")
        self.assertEqual(rows[0]["r"], "2.0")
        self.assertEqual(rows[1]["r"], "-1.0")
        s = journal.stats(rows)
        self.assertEqual(s["trades"], 3)
        self.assertEqual(s["net_pnl"], -2.0)
        self.assertEqual(s["max_losing_streak"], 2)
        self.assertEqual(s["max_drawdown"], 102.0)
        self.assertEqual(s["profit_factor"], round(100 / 102, 2))


class Risk(TmpDir):
    CFG = dict(check.DEFAULTS, account_balance=10000)

    def test_pass_and_blocks(self):
        tz = UTC
        now = datetime(2026, 11, 12, 10, tzinfo=UTC)
        p = econ.write_cache(econ.parse_events((FX / "ff_week.json").read_text()), 15)
        cal = json.loads(p.read_text())
        cal["updated_utc"] = "2026-11-12T08:00:00+00:00"
        p.write_text(json.dumps(cal))
        r = check.check(self.CFG, 2650, 2645, 0.2, tp=2660, spread=0.3, now=now, tz=tz)
        levels = {c["rule"]: c["level"] for c in r["checks"]}
        self.assertEqual(levels["risk per trade"], "PASS")
        self.assertEqual(levels["news"], "PASS")
        self.assertEqual(levels["journal"], "WARN")
        # 5 minutes before CPI (13:30 UTC)
        r = check.check(self.CFG, 2650, 2645, 0.2, tp=2660, now=datetime(2026, 11, 12, 13, 25, tzinfo=UTC), tz=tz)
        self.assertEqual(r["verdict"], "BLOCK")
        self.assertTrue(any(c["rule"] == "news blackout" for c in r["checks"]))
        # too big
        r = check.check(self.CFG, 2650, 2645, 1.0, tp=2660, now=now, tz=tz)
        self.assertEqual({c["rule"]: c["level"] for c in r["checks"]}["risk per trade"], "BLOCK")

    def test_daily_limits(self):
        now = datetime(2026, 11, 10, 10, tzinfo=UTC)
        for _ in range(3):
            journal.main(["add", "--side", "buy", "--entry", "2650", "--lots", "0.1", "--pnl", "-120",
                          "--open", "2026-11-10 09:00"])
        r = check.check(dict(self.CFG, timezone="UTC"), 2650, 2645, 0.1, tp=2660, now=now, tz=UTC)
        levels = {c["rule"]: c["level"] for c in r["checks"]}
        self.assertEqual(levels["trades today"], "BLOCK")
        self.assertEqual(levels["daily loss"], "BLOCK")


if __name__ == "__main__":
    unittest.main()
