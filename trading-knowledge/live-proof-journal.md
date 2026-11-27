# TradePilot Live Forward-Testing Proof Journal (Target: 30 Live Trades)
<!-- AUTO-LOG-MANAGED -->

Real-time automated forward proof of **TradePilot Dual-Engine Strategy** executed against live **Angel One SmartAPI** option quotes on the ₹1,00,000 simulated paper account.
_Last auto-sync: `2026-11-27 22:57:47 IST` • Auto-Paper-Trade: `ON` • Machine-readable log: [`live-trades.json`](./live-trades.json)_

## Live Running Scorecard

| Metric | Live Result (So Far) | 30-Trade Proof Target |
| --- | ---: | ---: |
| **Completed Live Trades** | **5 / 30** | 30+ |
| **Wins / Losses** | **2 W / 3 L (40.0%)** | ≥ 35% WR |
| **Gross Realized P&L** | **-₹901.50** | — |
| **Est. 2026 Charges (Brokerage + 0.15% STT + Taxes)** | **-₹493.84** | — |
| **Net Realized P&L** | **-₹1,395.34 (-1.40%)** | Positive (+8% to +15%+) |
| **Avg Win / Avg Loss (Net)** | **+₹2,964.58 / -₹2,441.50 (1.21×)** | ≥ 1.8× |
| **Profit Factor (Net)** | **0.81** | ≥ 1.25 |
| **Max Drawdown** | **₹7,324.50 (6.9%)** | ≤ ₹15,000 (15%) |

---

## Live Verified Trade Log

| # | Date | Entry → Exit (IST) | Instrument | Engine | Side | Qty | Entry (₹) | Exit (₹) | Pts | Exit Type | Gross P&L | Est. Charges | **Net P&L** |
| ---: | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| 1 | 2026-11-17 | 11:09:31 → 11:11:02 | `NIFTY17NOV2625400CE` | Manual | BUY | 65 | 63.50 | 69.35 | +5.85 | EXIT | +₹380.25 | ₹57.75 | **+₹322.50** |
| 2 | 2026-11-23 | 14:05:45 → 15:10:04 | `BANKNIFTY29DEC2663000PE` | MTF 20-EMA Pullback | BUY | 30 | 1,247.65 | 1,439.45 | +191.80 | EOD | +₹5,754.00 | ₹147.34 | **+₹5,606.66** |
| 3 | 2026-11-26 | 10:20:04 → 13:13:20 | `BANKNIFTY29DEC2663900CE` | MTF 20-EMA Pullback | BUY | 30 | 1,502.00 | 1,384.15 | -117.85 | SL/TARGET | -₹3,535.50 | ₹147.62 | **-₹3,683.12** |
| 4 | 2026-11-27 | 11:20:45 → 12:02:01 | `NIFTY01DEC2625700PE` | PDH/PDL Break & Hold | BUY | 65 | 167.70 | 140.35 | -27.35 | SL/TARGET | -₹1,777.75 | ₹69.72 | **-₹1,847.47** |
| 5 | 2026-11-27 | 12:25:05 → 12:48:46 | `NIFTY01DEC2625700PE` | PDH/PDL Break & Hold | BUY | 65 | 177.95 | 151.45 | -26.50 | SL/TARGET | -₹1,722.50 | ₹71.41 | **-₹1,793.91** |

---

## Daily Session Log (15:15 IST Auto-Check)

| Date | Trades | W / L | Net P&L | Auto-Trade | NIFTY (Spot / 15m Bias) | BANKNIFTY (Spot / 15m Bias) | Status |
| --- | ---: | :---: | ---: | :---: | --- | --- | --- |
| 2026-11-27 | 2 | 0 / 2 | -₹3,641.38 | ON | 25,607.2 / BEARISH | 63,040.9 / BEARISH | 2 trade(s) completed (0W/2L) • kill-switch hit |

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
