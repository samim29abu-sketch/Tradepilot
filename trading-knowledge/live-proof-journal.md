# TradePilot Live Forward-Testing Proof Journal (Target: 30 Live Trades)

Real-time automated forward proof of **TradePilot Dual-Engine Strategy** executed against live **Angel One SmartAPI** option quotes on the ₹1,00,000 simulated paper account (started **Monday, 23 Nov 2026**).

## Live Running Scorecard

| Metric | Live Result (So Far) | 30-Trade Proof Target |
| --- | ---: | ---: |
| **Completed Live Trades** | **1 / 30** | 30+ |
| **Wins / Losses** | **1 W / 0 L (100.0%)** | ≥ 35% WR |
| **Gross Realized P&L** | **+₹5,754.00** | — |
| **Est. 2026 Charges (Brokerage + 0.15% STT + Taxes)** | **-₹147.34** | — |
| **Net Realized P&L** | **+₹5,606.66 (+5.61%)** | Positive (+8% to +15%+) |
| **Avg Win / Avg Loss (Net)** | **+₹5,606.66 / —** | ≥ 1.8× |
| **Max Drawdown** | **₹0.00 (0.0%)** | ≤ ₹15,000 (15%) |

---

## Live Verified Trade Log

| # | Date | Entry → Exit (IST) | Instrument | Engine | Qty | Entry (₹) | Exit (₹) | Pts | Exit Type | Gross P&L | Est. Charges | **Net P&L** |
| ---: | --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| 1 | 2026-11-23 | 14:05:45 → 15:10:04 | `BANKNIFTY29DEC2663000PE` | MTF 20-EMA Pullback | 30 | 1,247.65 | 1,439.45 | +191.80 | EOD (15:10) | +₹5,754.00 | ₹147.34 | **+₹5,606.66** |

---

## Trade Notes & Model Audit

### Trade #1 — `2026-11-23` (`BANKNIFTY29DEC2663000PE`)
- **Execution Check:** Fully automated by Lightsail backend (`Auto-Paper-Trade: ON`).
- **Safety Checks Verified Live:**
  1. Skipped 09:15–09:30 opening crash and 11:30–13:15 midday chop cleanly.
  2. **Expiry-day rollover worked perfectly:** Rolled off 0-DTE `23NOV` expiry onto monthly `29DEC26` ATM strike (`63,000 PE`).
  3. Entered 45 seconds after 14:00 candle close (`14:05:45 IST`) and squared off cleanly 4 seconds after 15:10 IST (`15:10:04 IST`).
- **Model vs. Live Accuracy:**
  - Spot dropped `~396` pts; option gained **`+191.80` pts** → realized effective Delta = **`0.484`** (very close to our `0.55` backtest proxy on a 36-DTE contract).
  - Model predicted `+₹6,144` net; live real Angel One fill delivered **`+₹5,606.66` net** (within ~8% of model!).
- **Capital Check:** Buy value was `₹37,429.50` (~37.4% of ₹1L account — comfortable for 1 lot of next-month BANKNIFTY ATM).
