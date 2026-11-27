import datetime as dt
import json
from pathlib import Path
import tempfile
import unittest

import sync_trade_log as stl


class TestSyncTradeLog(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.json_path = self.root / "live-trades.json"
        self.md_path = self.root / "live-proof-journal.md"
        self.md_path.write_text(
            "# Old Header\n\n## Trade Notes & Model Audit\n\n### Trade #1\nManual audit preserved!\n",
            encoding="utf-8",
        )
        self.sample_state = {
            "realized": 5754.0,
            "estimatedCharges": 147.34,
            "positions": [],
            "scannerCfg": {"autoTrade": True, "maxDailyLoss": 3000, "maxDailyTrades": 4},
            "account": {"equity": 105754.0, "openPnl": 0.0},
            "daily": {"date": "2026-11-27", "killSwitchHit": False},
            "orders": [
                {"time": "2026-11-23T14:05:45+05:30", "symbol": "BANKNIFTY29DEC2663000PE", "side": "BUY",
                 "qty": 30, "price": 1247.65, "status": "FILLED", "pnl": None, "charges": None, "source": "SCANNER"},
                {"time": "2026-11-23T15:10:04+05:30", "symbol": "BANKNIFTY29DEC2663000PE", "side": "BUY",
                 "qty": 30, "price": 1439.45, "status": "EOD", "pnl": 5754.0, "charges": 147.34, "source": "SCANNER"},
            ],
        }
        self.sample_scanner = {
            "indices": {
                "NIFTY": {"spot": 25510.2, "htfBias": "BULLISH", "recentSetups": []},
                "BANKNIFTY": {"spot": 62840.5, "htfBias": "NEUTRAL", "recentSetups": []},
            }
        }

    def tearDown(self):
        self.tmp.cleanup()

    def test_first_sync_noop_and_preserves_notes_and_prior_sessions(self):
        fri_1516 = dt.datetime(2026, 11, 27, 15, 16, tzinfo=stl.IST)
        r1 = stl.sync_files(self.sample_state, self.sample_scanner, self.json_path, self.md_path, now=fri_1516)
        self.assertTrue(r1["changed"])
        self.assertEqual(r1["trades"], 1)
        self.assertEqual(r1["sessions"], 1)

        md = self.md_path.read_text(encoding="utf-8")
        self.assertIn("BANKNIFTY29DEC2663000PE", md)
        self.assertIn("+₹5,606.66", md)
        self.assertIn("2026-11-27", md)
        self.assertIn("0 trades — no valid 1:3 R:R trigger", md)
        self.assertIn("Manual audit preserved!", md)

        # Re-running 10 minutes later with identical state is a clean no-op
        r2 = stl.sync_files(
            self.sample_state, self.sample_scanner, self.json_path, self.md_path,
            now=dt.datetime(2026, 11, 27, 15, 26, tzinfo=stl.IST),
        )
        self.assertFalse(r2["changed"])

        # Next trading day (Mon Nov 30 at 15:16 IST) preserves Nov 27 session and adds Nov 30
        mon_1516 = dt.datetime(2026, 11, 30, 15, 16, tzinfo=stl.IST)
        r3 = stl.sync_files(self.sample_state, self.sample_scanner, self.json_path, self.md_path, now=mon_1516)
        self.assertTrue(r3["changed"])
        self.assertEqual(r3["sessions"], 2)
        saved = json.loads(self.json_path.read_text(encoding="utf-8"))
        self.assertEqual([s["date"] for s in saved["sessions"]], ["2026-11-27", "2026-11-30"])

    def test_skips_session_before_1515_on_holiday_and_weekend(self):
        for when in (
            dt.datetime(2026, 11, 27, 14, 30, tzinfo=stl.IST),  # before 15:15
            dt.datetime(2026, 11, 24, 15, 20, tzinfo=stl.IST),  # NSE holiday
            dt.datetime(2026, 11, 28, 15, 20, tzinfo=stl.IST),  # Saturday
        ):
            r = stl.sync_files(self.sample_state, self.sample_scanner, self.json_path, self.md_path, now=when)
            self.assertEqual(r["sessions"], 0)


if __name__ == "__main__":
    unittest.main()
